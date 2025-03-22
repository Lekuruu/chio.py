
from typing import Iterable, Tuple, Union
from .b20130604 import b20130604
from ..constants import *
from ..types import *
from ..io import *

class b20130801(b20130604):
    """
    b20130801 deprecates the "user is inactive" error, and is
    now interpreted as a "user is banned" error by clients.
    Chio will try to account for this by sending an announce
    packet with the original message.
    """
    version = 20130801

    @classmethod
    def write_login_reply(cls, reply: Union[int, LoginError]) -> Iterable[Tuple[PacketType, bytes]]:
        if reply is LoginError.UserInactive:
            # Clients interpret this as a "user is banned" error,
            # instead of the intended "user is inactive" error.
            reply = LoginError.InvalidLogin
            yield next(cls.write_announce(InactiveAccountMessage))

        yield next(super().write_login_reply(reply))
