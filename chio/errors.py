
class ChioError(Exception):
    """Base class for exceptions in Chio."""
    pass

class ChioReadError(ChioError):
    """Exception raised for errors reading from a client."""
    pass

class ChioWriteError(ChioError):
    """Exception raised for errors writing to a client."""
    pass

class InvalidPacketError(ChioError):
    """Exception raised for invalid packets."""
    pass
