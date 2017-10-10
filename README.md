## brogency/balancer [![Build Status](https://travis-ci.org/beda-software/balancer.svg?branch=master)](https://travis-ci.org/beda-software/balancer)


Load balancer build with etcd, confd and nginx, see configuration below.

Create host dir:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts -XPUT -d dir=true`

Create host config var:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world -XPUT -d -d dir=true`

Enable host:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/enable -XPUT -d value=True `

Set hostname:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/server_name -XPUT -d value=hello2.localhost`

Enable nginx base caches:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/caches/static/path -XPUT -d value="/static/"`
