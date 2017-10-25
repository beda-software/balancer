import pytest
import requests
import time
import docker
import re
import etcd
from contextlib import contextmanager


@pytest.fixture(scope='session')
def docker_client():
    return docker.from_env()


@pytest.fixture(scope='session')
def etcd_client():
    return etcd.Client(host='etcd', port=4001)


@pytest.fixture(scope='function')
def hello_world_service(docker_client, etcd_client):
    with wait_config_update(docker_client):
        container = docker_client.containers.run(
            'bedasoftware/hello-world',
            detach=True,
            network_mode='balancer_balancer')
        etcd_client.write('/hosts/hello-world/enable', True)
        etcd_client.write('/hosts/hello-world/server_name',
                          'hello-world.local')

    yield container

    container.kill()
    container.remove()
    try:
        etcd_client.delete('/hosts/hello-world/enable')
        etcd_client.delete('/hosts/hello-world/server_name')
    except etcd.EtcdKeyNotFound:
        pass


hello_world_service_2 = hello_world_service


def count_log_len(container):
    return len(container.logs().decode('utf-8').split('\n'))


@contextmanager
def wait_config_update(docker_client):
    container = [
        c for c in docker_client.containers.list()
        if c.name == 'balancer_confd_1'
    ][0]
    log_len = count_log_len(container)

    yield

    while True:
        for log in container.logs().decode('utf-8').split('\n')[log_len:]:
            if 'Target config /etc/nginx/conf.d/sites.conf has been updated' \
               in log:
                return
        time.sleep(1)


def test_nginx_is_available():
    resp = requests.get('http://confd/')
    assert resp.status_code == 200
    assert 'nginx' in resp.headers['Server']


def test_balancer_routing(hello_world_service):
    resp = requests.get('http://hello-world.local/')
    assert resp.status_code == 200
    assert 'Flask inside {0} at '.format(hello_world_service.id[:12])\
        == resp.content.decode('utf-8')

    resp = requests.get('http://confd/')
    assert resp.status_code == 200
    assert 'the nginx web server is successfully installed' \
        in resp.content.decode('utf-8')


def test_balancing(hello_world_service, hello_world_service_2):
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


@pytest.fixture
def cleanup_cache(etcd_client):
    yield lambda: etcd_client.write('/hosts/hello-world/caches/data/path',
                                    '/data/')

    etcd_client.delete('/hosts/hello-world/caches/data/path')


def test_caching(hello_world_service, etcd_client, docker_client, setup_cache):
    for _index in range(4):
        resp = requests.get('http://hello-world.local/')
        assert resp.status_code == 200
        assert 'Flask inside {0} at '.format(hello_world_service.id[:12])\
            == resp.content.decode('utf-8')
    assert count_log_len(hello_world_service) == 6

    with wait_config_update(docker_client):
        setup_cache()

    for _index in range(4):
        resp = requests.get('http://hello-world.local/data/index.html')
        assert resp.status_code == 200
        assert 'Flask inside {0} at data/index.html'.format(
            hello_world_service.id[:12]) == resp.content.decode('utf-8')

    assert count_log_len(hello_world_service) == 7
