
import re

OsuVersion = re.compile(
    r"^b(?P<date>\d{1,8})"
    r"(?:(?P<name>(?!dev|tourney|test|peppy|arcade|ubertest\b)\w+\b))?"
    r"(?:\.(?P<revision>\d{1,2}|))?"
    r"(?P<stream>dev|tourney|test|peppy|arcade|cuttingedge|beta|ubertest)?$"
)

EMAIL = re.compile(
    r"^[^@\s]{1,200}@[^@\s\.]{1,30}(?:\.[^@\.\s]{2,24})+$"
)

USERNAME = re.compile(
    r'^[a-zA-Z0-9|^\-{}_|\[\] ]+$'
)

DISCORD_USERNAME = re.compile(
    r'^[a-z0-9_-]{3,15}$'
)

URL = re.compile(
    r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
)

OSU_USER_AGENT = re.compile(
    r"^osu!*|Mozilla/\d+\.\d+ \(compatible; Clever Internet Suite \d+\.\d+\)$"
)
