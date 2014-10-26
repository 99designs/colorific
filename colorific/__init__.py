# define version
__version_info__ = {
    'major': 0,
    'minor': 3,
    'micro': 0,
    'releaselevel': 'final',
}


def get_version():
    """
    Return the formatted version information
    """
    vers = ["%(major)i.%(minor)i" % __version_info__, ]

    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s' % __version_info__)
    return ''.join(vers)

__version__ = get_version()

# import palette modules for backward compatilibity.
try:
    from .palette import *
    from .config import *

except ImportError:
    # you should install requirements, see requirements.pip file.
    pass
