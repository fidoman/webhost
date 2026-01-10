#!/bin/sh

set -e

pkg install py311-mako-1.3.5 apache24-2.4.62 php84 mysql80-server php84 php84-pecl-memcache-8.2 exim

# bitrix
pkg install php84-gd

# wiki
pkg install php84-mbstring php84-pecl-APCu-5.1.24 php84-xml php84-ctype php84-iconv php84-fileinfo php84-mysqli php84-intl

php -i | grep json
php -i | grep xml

php -i | grep xml
php -i | grep mbstring
php -i | grep mysqlnd
php -i | grep apcu
php -i | grep memcache

# wordpress
pkg install php84-filter

#apt install  php-json php-xml php-mbstring php-mysqlnd php-gd php-apcu

#apt install python3 python3-requests mysql-connector-python3
#apt install memcached

#a2enmod ssl
#a2enmod proxy-fcgi
#a2enmod rewrite
#a2enmod proxy_http

sed -i bak 's/^#\(LoadModule ssl_module\)/\1/' /usr/local/etc/apache24/httpd.conf
sed -i bak 's/^#\(LoadModule proxy_module\)/\1/' /usr/local/etc/apache24/httpd.conf
sed -i bak 's/^#\(LoadModule proxy_fcgi_module\)/\1/' /usr/local/etc/apache24/httpd.conf
sed -i bak 's/^#\(LoadModule proxy_http_module\)/\1/' /usr/local/etc/apache24/httpd.conf
sed -i bak 's/^#\(LoadModule rewrite_module\)/\1/' /usr/local/etc/apache24/httpd.conf

pkg install py311-certbot-3.0.1,1 py311-certbot-apache-3.0.1 python-3.11_3,2

#??? echo weekly_certbot_enable="YES" >> /etc/periodic.conf

echo ok
