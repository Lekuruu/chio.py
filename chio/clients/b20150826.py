
from typing import Union

from .b20141104 import b20141104
from ..constants import *

class b20150826(b20141104):
    """
    b20150826 adds the "Qualified" status to the beatmap info reply.
    """
    version = 20150826

    @classmethod
    def convert_ranked_status(cls, status: Union[RankedStatus, int]) -> int:
        if type(status) is int:
            # A custom status was sent
            return status

        # Loved status does not exist
        status_mapping = {
            RankedStatus.NotSubmitted: -1,
            RankedStatus.Pending: 0,
            RankedStatus.Ranked: 1,
            RankedStatus.Approved: 2,
            RankedStatus.Qualified: 3,
            RankedStatus.Loved: 2
        }
        return status_mapping.get(status, -1)
