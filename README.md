##brogency/balancer ![Buid Status](https://travis-ci.org/Brogency/balancer.svg?branch=master)

Load balanser build with etcd, conf and nginx, see configuration below.

Create host dir:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts -XPUT -d dir=true`

Create host config var:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world -XPUT -d -d dir=true`

Enable host:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/enable -XPUT -d value=True `

Set hostname:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/server_name -XPUT -d value=hello2.localhost`

Set media overriding:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/media -XPUT -d value=/home/helloworld/media`


Create static file serving:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/static/hello/enable -XPUT -d value=true`
`curl -L http://127.0.0.1:4001/v2/keys/hosts/static/hello/server_name -XPUT -d value="hello.world"`
`curl -L http://127.0.0.1:4001/v2/keys/hosts/static/hello/media -XPUT -d value="/var/www/hello"`

Enable nginx base caches:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/caches/static/path -XPUT -d value="/static/"`
