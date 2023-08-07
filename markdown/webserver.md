---
title: "webserver"
author: Giovanni Marelli
date: 2019-07-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# webserver

Configuration and experiences using webservers, here we show a deployment of wikimedia as example.

## webservers

### apache

Ligthweight, fast and reliable but complicated to configure and test.

### nginx

Same as apache but somehow easier to configure and test.
[configuration](https://github.com/sabeiro/sawmill/docker/webserver/)

```yaml
services:
  nginx:
    image: nginx:alpine
    #image: nginx:latest
    #restart: unless-stopped
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ${HOME}/certbot/conf:/etc/letsencrypt
      - ${HOME}/apache2:/etc/apache2
      - ${HOME}/certbot/www:/var/www/certbot
        #- /var/www/:/var/www/
      - ${HOME}/lav/siti:/var/www/html/
      - ${HOME}/log:/var/log/
    ports:
      - "80:80"
      - "443:443"
    networks:
      - webserver-net
```
Example of a default website:
```
server {
    listen   80; 
    listen   [::]:80; 
    server_name ${SERVER_PROD};
    # server_tokens off;
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;
    #error_log stderr notice;
    location /.well-known {
        root /var/www/certbot/;
        allow all;
    }
    return 301 https://${DOLLAR}host${DOLLAR}request_uri;
}
server {
    listen 443 ssl;
    server_name ${SERVER_PROD};
    server_tokens off;
   	root /var/www/html/;
    index index.html index.htm index.php;
    ssl_certificate /etc/letsencrypt/live/${SERVER_PROD}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${SERVER_PROD}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    location / {
        try_files ${DOLLAR}uri ${DOLLAR}uri/ =404;
        #proxy_set_header    Host                ${DOLLAR}http_host;
        #proxy_set_header    X-Real-IP           ${DOLLAR}remote_addr;
        #proxy_set_header    X-Forwarded-For     ${DOLLAR}proxy_add_x_forwarded_for;
    }
    location ~ /\.ht {
        deny all;
    }
}

```

### traefik

Only reverse-proxy with no webserver capability. Easy to configure but not completely reliable, I personally never understood why secure redirects weren't working and I dropped it.

Example of used [configuration](https://github.com/sabeiro/sawmill/docker/traefik/)

```yaml
services:
  traefik:
    image: "traefik:latest"
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "443:443"
    labels:
      traefik.enable: true
      traefik.port: 8080
      traefik.http.routers.traefik_https.rule: Host(`${SERVER_ROOT}`)
      traefik.http.routers.traefik_https.entrypoints: websecure
      traefik.http.routers.traefik_https.tls: true
      traefik.http.routers.traefik_https.tls.certResolver: lets-encrypt
      traefik.http.routers.traefik_https.service: api@internal
      traefik.backend: home
      traefik.frontend.rule: "PathPrefixStrip:/"
      traefik.port: 2015
      traefik.docker.network: ntw_front
      traefik.frontend.entryPoints: websecure
      #traefik.http.routers.traefik_https.middlewares: auth-dash
      #traefik.http.middlewares.auth-dash.basicauth.users: "admin:$$apr1$$.Mqpju24$OH9r.WHWHvUeUy3L0qsUM0"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - ./traefik/traefik.yml:/etc/traefik/traefik.yml:ro
      - ./traefik/traefik.d:/etc/traefik/traefik.d:ro
      - ./traefik/acme.json:/acme.json:rw
      - ./letsencrypt:/etc/letsencrypt
      - ../../logs/:/logs/
    networks: 
      - traefik-net
```

# certificate

We use certbot (let'e encrypt)

```yaml
services:
  certbot:
    image: certbot/certbot
    restart: unless-stopped
    volumes:
      - ${HOME}/certbot/conf:/etc/letsencrypt
      - ${HOME}/certbot/www:/var/www/certbot
      - ${HOME}/log/:/var/log/
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
    networks:
      - webserver-net
```

Example for [docker-compose](https://github.com/sabeiro/sawmill/docker/webserver/init-letsencrypt.sh):
```
docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot
echo
```


# php

[Dockerfile](https://github.com/sabeiro/sawmill/webserver/php/:
```
FROM php:7.4-fpm
RUN apt-get update && apt-get install -y \
		libfreetype6-dev \
		libjpeg62-turbo-dev \
		libpng-dev \
	&& docker-php-ext-configure gd --with-freetype --with-jpeg \
	&& docker-php-ext-install -j$(nproc) gd

WORKDIR /var/www/html
COPY selections.conf selections.conf
RUN apt-get install debconf-utils
RUN debconf-set-selections < selections.conf
#RUN dpkg-reconfigure keyboard-configuration -f noninteractive
RUN apt install -y libicu-dev
RUN apt install -y lilypond imagemagick ghostscript fluidsynth firejail lame

RUN docker-php-ext-configure intl
RUN docker-php-ext-install gd pdo pdo_mysql mysqli intl
RUN docker-php-ext-enable pdo_mysql intl
#RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN usermod -u 1000 www-data
USER www-data

EXPOSE 9000
CMD ["php-fpm"]
```

Webserver configuration to route all the php requests to the php container:


```
upstream php_upstream {
	server php-app:9000 fail_timeout=5s max_fails=5;
}
server {
	...
	location ~ \.php${DOLLAR} {
      try_files ${DOLLAR}uri =404;
      fastcgi_split_path_info ^(.+\.php)(/.+)${DOLLAR};
      fastcgi_pass php_upstream;
      fastcgi_index index.php;
      fastcgi_param SCRIPT_FILENAME ${DOLLAR}document_root${DOLLAR}fastcgi_script_name;
      include /etc/nginx/fastcgi_params;
      include fastcgi.conf;
      #include fastcgi_params;
      fastcgi_param PATH_INFO ${DOLLAR}fastcgi_path_info;
   }
}
```

# load balancing

Redis, celery...
