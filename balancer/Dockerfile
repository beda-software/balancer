FROM nginx:1.11

WORKDIR /usr/local/bin
RUN apt-get update
RUN apt-get install -y curl

RUN curl -L https://github.com/kelseyhightower/confd/releases/download/v0.10.0/confd-0.10.0-linux-amd64 -o /usr/local/bin/confd
RUN chmod +x /usr/local/bin/confd

RUN mkdir -p /etc/confd/templates
RUN mkdir -p /etc/confd/conf.d
RUN mkdir -p /data/nginx/cache/

ADD nginx.conf /etc/nginx/nginx.conf
ADD confd/nginx.tmpl /etc/confd/templates/nginx.tmpl
ADD confd/nginx.toml /etc/confd/conf.d/nginx.toml

ADD confd-watch /usr/local/bin/confd-watch
CMD ["/usr/local/bin/confd-watch"]
