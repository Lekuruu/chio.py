
from ..chio import BanchoIO
from .b282 import b282
from .b291 import b291
from .b294 import b294
from .b296 import b296
from .b298 import b298
from .b312 import b312
from .b320 import b320
from .b323 import b323
from .b334 import b334
from .b338 import b338
from .b340 import b340
from .b342 import b342
from .b349 import b349
from .b354 import b354
from .b374 import b374
from .b388 import b388
from .b402 import b402

ClientDict = {
    282: b282(), 290: b282(),
    291: b291(), 293: b291(),
    294: b294(), 295: b294(),
    296: b296(), 297: b296(),
    298: b298(), 311: b298(),
    312: b312(), 319: b312(),
    320: b320(), 322: b320(),
    323: b323(), 333: b323(),
    334: b334(), 337: b334(),
    338: b338(), 339: b338(),
    340: b340(), 341: b340(),
    342: b342(), 348: b342(),
    349: b349(), 353: b349(),
    354: b354(), 373: b354(),
    374: b374(), 387: b374(),
    388: b388(), 401: b388(),
    402: b402()
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
