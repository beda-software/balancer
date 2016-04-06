import pytest
import requests
import time

from lxml import html


@pytest.fixture(scope='function')
def tutum_hello_world(request):
    from docker import Client
    cli = Client(base_url='unix://var/run/docker.sock')
    cli.pull('tutum/hello-world')
    container = cli.create_container(
        image='tutum/hello-world')
    cli.start(container=container.get('Id'))

    def stop():
        cli.stop(container)
        cli.remove_container(container)

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


def test_balance_routing(tutum_hello_world, etcd):
    etcd.write('/hosts/hello-world/enable', True)
    etcd.write('/hosts/hello-world/server_name', 'confd')

    time.sleep(1)  # Wait for confd

    resp = requests.get('http://confd/')
    assert resp.status_code == 200

    tree = html.fromstring(resp.content)
    title = tree.xpath('//title/text()')[0]
    container_id = tree.xpath('//h3/text()')[0][-12:]

    assert title == 'Hello world!'
    assert container_id == tutum_hello_world['Id'][:12]
