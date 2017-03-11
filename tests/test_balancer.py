import pytest
import requests
import time
import docker


client = docker.from_env()


@pytest.fixture(scope='function')
def hello_world_service(request):
    container = client.containers.run(
        'brogency/hello-world',
        detach=True,
        network_mode='balancer_default')

    def stop():
        container.kill()
        container.remove()

    request.addfinalizer(stop)
    return container


@pytest.fixture(scope='module')
def etcd(request):
    import etcd
    return etcd.Client(host='etcd', port=4001)


def test_nginx_is_available():
    resp = requests.get('http://confd/')
    assert resp.status_code == 200
    assert 'nginx' in resp.headers['Server']


def test_balance_routing(hello_world_service, etcd):
    etcd.write('/hosts/hello-world/enable', True)
    etcd.write('/hosts/hello-world/server_name', 'confd')

    time.sleep(10)  # Wait for confd

    resp = requests.get('http://confd/')
    assert resp.status_code == 200
    assert 'Flask inside {0}'.format(hello_world_service.id[:12]) == resp.content.decode('utf-8')
