
from typing import Iterable, Tuple, Union
from .b20160404 import b20160404
from ..constants import *
from ..types import *
from ..io import *

class b20161101(b20160404):
    """
    b20161101 introduced the loved status to the beatmap info reply.
    """
    version = 20161101

    @classmethod
    def convert_ranked_status(cls, status: Union[RankedStatus, int]) -> int:
        return status
