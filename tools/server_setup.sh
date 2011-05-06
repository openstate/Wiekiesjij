#!/bin/bash
################
# Stackscript Getlogic used on Linode converted to work on the new HNS server
# NOTE: This script does not install MySQL, as we have that on it's own server
#
################

HOSTNAME='host62'
NGINX_VERSION='0.8.54'
MONIT_VERSION='5.2.4'
MONITORING_IP='178.79.128.92'

# Upgrade system
apt-get update
apt-get -y upgrade
apt-get -y install vim less mc ack htop gettext zsh mailutils subversion curl
apt-get -y install libpcre3-dev build-essential libssl-dev libjpeg62-dev libreadline-dev

# Install local postfix
echo "postfix postfix/main_mailer_type select Internet Site" | debconf-set-selections
echo "postfix postfix/mailname string localhost" | debconf-set-selections
echo "postfix postfix/destinations string localhost.localdomain, localhost" | debconf-set-selections
apt-get -y install postfix
/usr/sbin/postconf -e "inet_interfaces = loopback-only"
/usr/sbin/postconf -e "local_transport = error:local delivery is disabled"
/etc/init.d/postfix restart

# Set timezone
echo "Europe/Amsterdam" | tee /etc/timezone
dpkg-reconfigure --frontend noninteractive tzdata

# Django setup
apt-get -y install mercurial git-core bzr memcached
apt-get -y install python python-dev python-setuptools python-psycopg2 python-imaging python-virtualenv python-mysqldb
easy_install -U distribute pip
pip install virtualenv
mkdir /var/projects


# Nginx setup

# Dependencies
adduser --system --no-create-home --disabled-login --disabled-password --group nginx

# Dopwnload and compile
cd /usr/src
curl -O http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz
tar xzf nginx-$NGINX_VERSION.tar.gz
cd /usr/src/nginx*
./configure --prefix=/opt/nginx --user=nginx --group=nginx --with-http_ssl_module --with-http_realip_module --with-http_stub_status_module
make
make install

# Init scripts
curl -O http://library.linode.com/assets/634-init-deb.sh
mv 634-init-deb.sh /etc/init.d/nginx
chmod +x /etc/init.d/nginx
/usr/sbin/update-rc.d -f nginx defaults

# Create project directories
mkdir /opt/nginx/conf/{sites-enabled,sites-available}
ln -s /opt/nginx/logs /var/log/nginx

echo "
user nginx nginx;
worker_processes 4;

error_log /var/log/nginx/error.log notice;
pid /var/run/nginx.pid;

events {
	worker_connections 1024;
	use epoll;
}

http {
	include mime.types;
	include proxy.conf;
	default_type application/octet-stream;

	log_format main  '\$remote_addr - \$remote_user [\$time_local] '
					 '\"\$request\" \$status \$body_bytes_sent \"\$http_referer\" '
					 '\"\$http_user_agent\" \"\$upstream_response_time ms\"';
	server_tokens off;

	sendfile    on;
	tcp_nopush  on;
	tcp_nodelay on;

	gzip                on;
	gzip_http_version   1.1;
	gzip_comp_level     2;
	gzip_proxied        any;
	gzip_types          text/plain text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript;

    server {
		listen 127.0.0.1;
		server_name localhost;
		location /nginx_status {
			stub_status on;
			access_log off;
			allow 127.0.0.1;
			deny all;
		}
	}


	include /opt/nginx/conf/sites-enabled/*;
}
" > /opt/nginx/conf/nginx.conf

echo "
	server {
		listen 80 default;
		server_name _;
		server_name_in_redirect off;
		root /opt/nginx/html/;
	}
" > /opt/nginx/conf/sites-available/default
ln -s /opt/nginx/conf/sites-available/default /opt/nginx/conf/sites-enabled

echo "
proxy_redirect     off;
proxy_set_header   Host             \$host;
proxy_set_header   X-Real-IP        \$remote_addr;
proxy_set_header   X-Forwarded-For  \$proxy_add_x_forwarded_for;

client_max_body_size       10m;
client_body_buffer_size    128k;
" > /opt/nginx/conf/proxy.conf
	/etc/init.d/nginx start




# Dependencies
apt-get -y install flex bison monit

# Download and compile
cd /usr/src
curl -O http://mmonit.com/monit/dist/monit-$MONIT_VERSION.tar.gz
tar xzf monit-$MONIT_VERSION.tar.gz
cd /usr/src/monit*
./configure --prefix=/opt/monit --sysconfdir=/etc/monit
make
make install

# Use ubuntu init scripts
apt-get -y remove monit
chmod +x /etc/init.d/monit
/usr/sbin/update-rc.d -f monit defaults

echo "
set daemon 60
  with start delay 70

set logfile syslog

set eventqueue basedir /var/monit slots 1000
set mmonit http://monitor:@$MONITORING_IP:8080/collector
set httpd port 2812 and use address 0.0.0.0
  allow 443jn34F3rwrewrrf3r3rFDf:\"FDSFf3f43r3qcko4t435%efdfgdfgd\"
  allow localhost
  allow $MONITORING_IP

include /etc/monit/conf.d/*.conf

check system getavoice
  if loadavg (5min) > 2 then alert
  if memory usage > 90% then alert

check process sshd
  with pidfile \"/var/run/sshd.pid\"
  start program \"/etc/init.d/ssh start\"
  stop program \"/etc/init.d/ssh stop\"
  if failed port 22 protocol ssh then restart
  if 5 restarts within 5 cycles then timeout

" > /etc/monit/monitrc

#Nginx
echo "
check process nginx
  with pidfile \"/var/run/nginx.pid\"
  start program = \"/etc/init.d/nginx start\"
  stop program = \"/etc/init.d/nginx stop\"
  if failed host 0.0.0.0 port 80 protocol http for 2 cycles then restart
" >> /etc/monit/monitrc

#memcache
echo "
check process memcached
  with pidfile \"/var/run/memcached.pid\"
  start program = \"/etc/init.d/memcached start\"
  stop program = \"/etc/init.d/memcached stop\"
  if failed port 11211 protocol memcache for 2 cycles then restart
" >> /etc/monit/monitrc

echo "
check process postfix
  with pidfile \"/var/spool/postfix/pid/master.pid\"
  start program = \"/etc/init.d/postfix start\"
  stop program = \"/etc/init.d/postfix stop\"
  if failed port 25 protocol smtp for 2 cycles then restart
" >> /etc/monit/monitrc

echo "startup=1" > /etc/default/monit


apt-get -y install munin-node libwww-perl
cd /etc/munin/plugins/
rm -f *
ln -sf /usr/share/munin/plugins/cpu
ln -sf /usr/share/munin/plugins/df
ln -sf /usr/share/munin/plugins/diskstats
ln -sf /usr/share/munin/plugins/if_ if_eth0
ln -sf /usr/share/munin/plugins/if_err_ if_err_eth0
ln -sf /usr/share/munin/plugins/load
ln -sf /usr/share/munin/plugins/memory
ln -sf /usr/share/munin/plugins/open_files
ln -sf /usr/share/munin/plugins/open_inodes
ln -sf /usr/share/munin/plugins/processes
ln -sf /usr/share/munin/plugins/swap
ln -sf /usr/share/munin/plugins/uptime
ln -sf /usr/share/munin/plugins/threads
ln -sf /usr/share/munin/plugins/users
ln -sf /usr/share/munin/plugins/nginx_request
ln -sf /usr/share/munin/plugins/nginx_status

echo "
log_level 4
log_file /var/log/munin/munin-node.log
pid_file /var/run/munin/munin-node.pid

background 1
setsid 1

user root
group root

ignore_file ~$
ignore_file DEADJOE$
ignore_file \.bak$
ignore_file %$
ignore_file \.dpkg-(tmp|new|old|dist)$
ignore_file \.rpm(save|new)$
ignore_file \.pod$

host_name $HOSTNAME

allow ^127\.0\.0\.1$
allow ^$MONITORING_IP$

host *
port 4949
" > /etc/munin/munin-node.conf

stop munin-node
start munin-node

# Setup firewall
iptables -A INPUT -p tcp -s $MONITORING_IP --dport 4949 -j ACCEPT
iptables -A INPUT -p tcp -s $MONITORING_IP --dport 2812 -j ACCEPT
