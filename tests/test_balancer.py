import pytest
import requests
import time
import docker
import re
from contextlib import contextmanager

client = docker.from_env()


def count_log_len(container):
    return len(container.logs().decode('utf-8').split('\n'))


@contextmanager
def wait_config_update():
    container = [
        c for c in client.containers.list() if c.name == 'balancer_confd_1'
    ][0]
    log_len = count_log_len(container)

    yield

    while 'Target config /etc/nginx/conf.d/sites.conf has been updated' \
          not in container.logs().decode('utf-8').split('\n')[-2] or \
          log_len == count_log_len(container):
        time.sleep(1)


@pytest.fixture(scope='function')
def hello_world_service(request):
    container = client.containers.run('bedasoftware/hello-world',
                                      detach=True,
                                      network_mode='balancer_balancer')

    def stop():
        container.kill()
        container.remove()

    request.addfinalizer(stop)
    return container


hello_world_service_2 = hello_world_service


@pytest.fixture(scope='module')
def etcd(request):
    import etcd
    return etcd.Client(host='etcd', port=4001)


def test_nginx_is_available():
    resp = requests.get('http://confd/')
    assert resp.status_code == 200
    assert 'nginx' in resp.headers['Server']


def test_balancer_routing(hello_world_service, etcd):
    with wait_config_update():
        etcd.write('/hosts/hello-world/enable', True)
        etcd.write('/hosts/hello-world/server_name', 'hello-world.local')

    resp = requests.get('http://hello-world.local/')
    assert resp.status_code == 200
    assert 'Flask inside {0} at '.format(hello_world_service.id[:12])\
        == resp.content.decode('utf-8')

    resp = requests.get('http://confd/')
    assert resp.status_code == 200
    assert 'the nginx web server is successfully installed' \
        in resp.content.decode('utf-8')


def test_balancing(hello_world_service, hello_world_service_2, etcd):
    with wait_config_update():
        etcd.write('/hosts/hello-world/enable', True)
        etcd.write('/hosts/hello-world/server_name', 'hello-world.local')

    ids = {
        hello_world_service.id[:12]: False,
        hello_world_service_2.id[:12]: False,
    }

    for _index in range(4):
        resp = requests.get('http://hello-world.local/')
        assert resp.status_code == 200
        res = re.search(r'^Flask inside ([\w\d]+)',
                        resp.content.decode('utf-8'))
        ids[res.groups()[0]] = True

    assert all(ids.values())


def test_caching(hello_world_service, etcd):
    with wait_config_update():
        etcd.write('/hosts/hello-world/enable', True)
        etcd.write('/hosts/hello-world/server_name', 'hello-world.local')

    for _index in range(4):
        resp = requests.get('http://hello-world.local/')
        assert resp.status_code == 200
        assert 'Flask inside {0} at '.format(hello_world_service.id[:12])\
            == resp.content.decode('utf-8')
    assert len(hello_world_service.logs().decode('utf-8').split('\n')) \
        == 6

    with wait_config_update():
        etcd.write('/hosts/hello-world/caches/data/path', '/data/')

    for _index in range(4):
        resp = requests.get('http://hello-world.local/data/index.html')
        assert resp.status_code == 200
        assert 'Flask inside {0} at data/index.html'.format(
            hello_world_service.id[:12]) == resp.content.decode('utf-8')

    assert len(hello_world_service.logs().decode('utf-8').split('\n')) \
        == 7
