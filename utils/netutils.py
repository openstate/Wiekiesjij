"""
Common IP adress utilities.

Settings:
    NETUTILS_CACHE -- django.core.cache.get_cache string defining the cache to use
    By default django.core.cache.cache will be used.

    NETUTILS_UNIQUE_VISITOR_TIMEOUT -- datetime.timedelta defining timeout between
    visits to count the user as unique visitor.

@author Sardar Yumatov (ja.doma@gmail.com)

"""

import socket
import struct
import datetime
import cPickle as pickle

from django.conf import settings


# init cache
if getattr(settings, 'NETUTILS_CACHE', None):
    from django.core.cache import get_cache
    cache = get_cache(settings.NETUTILS_CACHE)
    
else:
    # use default cache
    from django.core.cache import cache



def ip2long(ip):
    """ Converts IPv4 address to integer (32-bit) in host byte order """
    (g, ) = struct.unpack('I', socket.inet_aton(ip))
    return socket.ntohl(g)

def long2ip(num):
    """ Converts 32-bits integer to IPv4 address """
    return socket.inet_ntoa(struct.pack('I', socket.ntohl(num)))


# Reserved IP ranges (Wikipedia)
RESERVED_IP = [
    ('0.0.0.0', '0.255.255.255'),       # 0.0.0.0/8     Zero Addresses (RFC 1700)
    ('10.0.0.0', '10.255.255.255'),     # 10.0.0.0/8 	Private IP addresses (RFC 1918)
    ('127.0.0.0','127.255.255.255'),    # 127.0.0.0/8 	Localhost Loopback Address (RFC 1700)
    ('169.254.0.0', '169.254.255.255'), # 169.254.0.0/16  Zeroconf / APIPA (RFC 3330)
    ('172.16.0.0', '172.31.255.255'),   # 172.16.0.0/12 Private IP addresses (RFC 1918)
    ('192.0.2.0', '192.0.2.255'),       # 192.0.2.0/24 	Documentation and Examples (RFC 3330)
    ('192.88.99.0', '192.88.99.255'),   # 192.88.99.0/24 IPv6 to IPv4 relay Anycast (RFC 3068)
    ('192.168.0.0','192.168.255.255'),  # 192.168.0.0/16 Private IP addresses (RFC 1918)
    ('198.18.0.0', '198.19.255.255'),   # 198.18.0.0/15 Network Device Benchmark (RFC 2544)
    ('224.0.0.0', '239.255.255.255'),   # 224.0.0.0/4   Multicast (RFC 3171)
]
# convert to min/max ranges for speedup
RESERVED_IP_INT = [(ip2long(mn), ip2long(mx)) for (mn, mx) in RESERVED_IP]


def is_valid_remote_ip(ip):
    """
        Returns true if given IPv4 address is of correct syntax and is not
        in reserved range.

        @param ip IPv4 address in dotted notation (eg. 123.123.123.123)
        @return bool True if given ip can be a remote IP
    """
    if ip is None:
        return False
    
    ip = str(ip)
    if ip == "":
        return False
    
    try:
        ip = ip2long(ip)

        for (mn, mx) in RESERVED_IP_INT:
            if ip >= mn and ip <= mx:
                return False

        return True
    except:
        return False



def getip(request):
    """ Returns IPv4 adress from request.META """
    meta = request.META

    if 'HTTP_CLIENT_IP' in meta and is_valid_remote_ip(meta['HTTP_CLIENT_IP']):
        return meta['HTTP_CLIENT_IP']

    # common proxy headers
    if 'HTTP_X_FORWARDED' in meta and is_valid_remote_ip(meta['HTTP_X_FORWARDED']):
        return meta['HTTP_X_FORWARDED']

    if 'HTTP_FORWARDED' in meta and is_valid_remote_ip(meta['HTTP_FORWARDED']):
        return meta['HTTP_FORWARDED']
    
    if 'HTTP_X_FORWARDED_FOR' in meta or 'HTTP_FORWARDED_FOR' in meta:
        # this is a ',' separated list of IP's along all proxies with client
        # being the first and each proxy appended right
        # the client IP is usually invalid (internal/reserved), so try to
        # identify his/her nearest proxy
        ls = meta['HTTP_FORWARDED_FOR'] if 'HTTP_FORWARDED_FOR' in meta else meta['HTTP_X_FORWARDED_FOR']
        for ip in ls.split(','):
            if is_valid_remote_ip(ip):
                return ip
    # end forwarded for

    if 'REMOTE_ADDR' in meta and is_valid_remote_ip(meta['REMOTE_ADDR']):
        return meta['REMOTE_ADDR']
    
    # no valid IP found
    return None



def check_remote_timeout(timeout, request, key = None):
    """
        Returns True if the time elapsed between request from the same
        (key, remote user) is larger than given timeout.

        Note: key is used to distinguish the services restricting the access to
        the same user. For example a 'wiki' service can block the user from
        posting new article for 15 minutes, this timeout should not prevent the
        user to post a message in 'forum'.

        Note: this function is not strictly thread-safe, it depends on underlying
        cache implementation.

        @param timeout the timeout as datetime.timedelta
        @param request used for request.META dict
        @param key service name, any string key
        @return bool True if timeout is passed, False otherwise
    """
    # treat all users with unrecognized IP as a single user with "unknown ip"
    strkey = pickle.dumps((getip(request), key)) # will be hashed anyway
    val = cache.get(strkey)

    # expired
    if val is None or (val + timeout) < datetime.datetime.now():
        cache.set(strkey, datetime.datetime.now())
        return True

    return False



def check_unique_visitor(request, key = None):
    """
        Returns True once in a day for the remote user.

        @see check_remote_timeout()
        @param request used for request.META
        @param key the service name, any string key
        @return bool True if more than a day is elapsed between calls for given remote user
    """
    if getattr(settings, 'NETUTILS_UNIQUE_VISITOR_TIMEOUT', None):
        timeout = settings.NETUTILS_UNIQUE_VISITOR_TIMEOUT
    else:
        timeout = datetime.timedelta(days = 1)

    return check_remote_timeout(timeout, request, key)


