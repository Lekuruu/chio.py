
from typing import Dict
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
from .b425 import b425
from .b452 import b452
from .b470 import b470
from .b487 import b487
from .b489 import b489
from .b490 import b490
from .b504 import b504
from .b535 import b535
from .b558 import b558
from .b591 import b591
from .b613 import b613
from .b634 import b634
from .b695 import b695
from .b1183 import b1183
from .b1365 import b1365
from .b1600 import b1600
from .b1788 import b1788
from .b1796 import b1796
from .b1797 import b1797
from .b1817 import b1817
from .b20120518 import b20120518
from .b20120703 import b20120703
from .b20120723 import b20120723
from .b20120725 import b20120725
from .b20120806 import b20120806
from .b20120818 import b20120818
from .b20121023 import b20121023
from .b20121028 import b20121028
from .b20121203 import b20121203
from .b20121207 import b20121207
from .b20121211 import b20121211
from .b20121212 import b20121212
from .b20121224 import b20121224
from .b20121225 import b20121225
from .b20130118 import b20130118

ClientDict: Dict[int, BanchoIO] = {
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
    402: b402(), 424: b402(),
    425: b425(), 451: b425(),
    452: b452(), 469: b452(),
    470: b470(), 486: b470(),
    487: b487(), 488: b487(),
    489: b489(),
    490: b490(), 503: b490(),
    504: b504(), 535: b504(),
    535: b535(), 557: b535(),
    558: b558(), 590: b558(),
    591: b591(), 612: b591(),
    613: b613(), 633: b613(),
    634: b634(), 678: b634(),
    695: b695(), 1182: b695(),
    1183: b1183(), 1364: b1183(),
    1365: b1365(), 1599: b1365(),
    1600: b1600(), 1787: b1600(),
    1788: b1788(), 1795: b1788(),
    1796: b1796(), 1797: b1797(),
    1817: b1817(), 20120517: b1817(),
    20120518: b20120518(), 20120702: b20120518(),
    20120703: b20120703(), 20120722: b20120703(),
    20120723: b20120723(), 20120724: b20120723(),
    20120725: b20120725(), 20120805: b20120725(),
    20120806: b20120806(), 20120817: b20120806(),
    20120818: b20120818(), 20121022: b20120818(),
    20121023: b20121023(), 20121027: b20121023(),
    20121028: b20121028(), 20121202: b20121028(),
    20121203: b20121203(), 20121206: b20121203(),
    20121207: b20121207(), 20121210: b20121207(),
    20121211: b20121211(), 20121212: b20121212(),
    20121223: b20121212(), 20121224: b20121224(),
    20121225: b20121225(), 20130117: b20121225(),
    20130118: b20130118()
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

def set_protocol_version(client: int, version: int) -> None:
    ClientDict[client].protocol_version = version
