
from ..chio import BanchoIO
from .b282 import b282
from .b291 import b291
from .b294 import b294

ClientDict = {
    282: b282(), 290: b282(),
    291: b291(), 293: b291(),
    294: b294(), 295: b294(),
}

HighestVersion = max(ClientDict.keys())
LowestVersion = min(ClientDict.keys())

def select_client(version: int) -> BanchoIO:
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
