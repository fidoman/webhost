apt install python3-mako apache2 php-fpm default-mysql-server
apt install php-fpm apache2-dev pkg-config php-mbstring php-xml php-intl php-pgsql
# bitrix
apt install php-gd

# wiki
apt install php-fpm php-json php-xml php-mbstring php-mysqlnd php-gd php-apcu
#apt install python3 python3-requests mysql-connector-python3
apt install memcached

a2enmod dav_lock dav_fs speling auth_digest proxy_fcgi authn_socache
a2enmod ssl
a2enmod proxy-fcgi
a2enmod rewrite
a2enmod proxy_http

#mkdir /var/log/php/
#chgrp www-data /var/log/php/
#chmod g+rwx /var/log/php/

#mkdir /var/php
#chgrp www-data /var/log/php/
#chgrp www-data /var/run/apache2 # cgid

