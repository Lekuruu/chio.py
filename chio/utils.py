
from .clients import ClientDict, LowestVersion, HighestVersion
from .chio import BanchoIO

def select_client(version: int) -> BanchoIO:
    """Select the appropriate client based on the version provided."""
    if version in ClientDict:
        return ClientDict[version]
    
    if version < LowestVersion:
        return ClientDict[LowestVersion]
    
    if version > HighestVersion:
        return ClientDict[HighestVersion]
    
    for client_version, client in ClientDict.items():
        if version < client_version:
            return client

    # This should never happen, but just in case
    return ClientDict[HighestVersion]

def select_latest_client() -> BanchoIO:
    """Select the latest client available."""
    return ClientDict[HighestVersion]

def select_initial_client() -> BanchoIO:
    """Select the oldest client available."""
    return ClientDict[LowestVersion]
