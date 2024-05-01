
__author__ = 'Lekuru'
__email__ = 'contact@lekuru.xyz'
__version__ = '1.0.0'
__license__ = 'MIT'

from . import constants
from . import objects

from .versions.b20130815 import ResponsePacket as DefaultResponsePacket
from .versions.b20130815 import RequestPacket as DefaultRequestPacket

from .chio import MULTIPLAYER_MAX_SLOTS
from .chio import encode, decode
