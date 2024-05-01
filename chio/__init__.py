
__author__ = 'Lekuru'
__email__ = 'contact@lekuru.xyz'
__version__ = '1.0.0'
__license__ = 'MIT'

from . import constants
from . import objects

from .versions.b20130815 import ResponsePacket
from .versions.b20130815 import RequestPacket

from .chio import MULTIPLAYER_MAX_SLOTS
from .chio import encode, decode
