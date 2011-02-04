user = '%(user_name)s'
group = '%(user_name)s'
bind = 'unix:///var/run/%(hostname)s.sock'
pidfile = '/var/run/%(hostname)s.pid'
workers = '9'
deamon = True
worker_class = 'gevent'
