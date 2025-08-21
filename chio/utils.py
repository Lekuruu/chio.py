
from .clients import ClientDict, LowestVersion, HighestVersion
from .constants import CountryAcronyms, ChatLinkModern
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

format_link_basic = lambda m: f"{m.group(2)} ({m.group(1)})"
format_link_markdown = lambda m: f"({m.group(2)})[{m.group(1)}]"

def format_chat_message_to_markdown(message: str) -> str:
    """Run a filter that converts modern chat links to the legacy, markdown-ish format."""
    matches = ChatLinkModern.findall(message)

    if not matches:
        return message

    # NOTE: The client can only handle one singular chat link, per message
    #       We want to make sure we are keeping the link for the last message
    #       but replace all others with their regular link text without URL
    #       Example: "[http://osu.ppy.sh osu!] is a game about [http://en.wikipedia.org/wiki/Circle circles]"
    #                -> "osu! (http://osu.ppy.sh) is a game about (circles)[http://en.wikipedia.org/wiki/Circle]"

    if len(matches) <= 1:
        # If there's only one match, return it formatted
        return ChatLinkModern.sub(format_link_markdown, message, count=1)

    # Use "basic" formatter except for the last
    text = ChatLinkModern.sub(format_link_basic, message, count=len(matches) - 1)
    
    # Format last with the legacy/markdown chat link format
    return ChatLinkModern.sub(format_link_markdown, text, count=1)
