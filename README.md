## brogency/balancer [![Build Status](https://travis-ci.org/beda-software/balancer.svg?branch=master)](https://travis-ci.org/beda-software/balancer)


Load balancer build with etcd, confd and nginx, see configuration below.  

Create host config var:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world -XPUT -d dir=true`  

Set hostname:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/server_name -XPUT -d value=hello-world.local`  


Enable host:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/enable -XPUT -d value=True `  

Enable nginx base caches:  
`curl -L http://127.0.0.1:4001/v2/keys/hosts/hello-world/caches/assets/path -XPUT -d value="/assets/"`  
