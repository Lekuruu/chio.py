from .b20130801 import b20130801

class b20140528(b20130801):
    """
    b20140528 allows for 16-player multiplayer matches, if
    the protocol version is set to 19 or higher.
    """
    version = 20140528
    protocol_version = 18
    slot_size = 16

    @classmethod
    def read_match(cls, stream):
        cls.slot_size = 16 if cls.protocol_version >= 19 else 8
        return super().read_match(stream)

    @classmethod
    def write_match(cls, match):
        cls.slot_size = 16 if cls.protocol_version >= 19 else 8
        return super().write_match(match)
