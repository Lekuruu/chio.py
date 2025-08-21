
from .clients import ClientDict, LowestVersion, HighestVersion
from .constants import CountryAcronyms
from .chio import BanchoIO

def resolve_country_index(country_acronym: str) -> int:
    """
    Resolve the country index from the acronym.
    If the acronym is not found, it will return 0.
    """
    return (
        CountryAcronyms.index(country_acronym)
        if country_acronym in CountryAcronyms else 0
    )

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
