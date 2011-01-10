try:
    from settings.local_settings import *
except ImportError:
    from settings.default_settings import *
    