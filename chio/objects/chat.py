
from dataclasses import dataclass

@dataclass
class Message:
    sender: str
    content: str
    target: str
    sender_id: int = 0
    is_private: bool = False

@dataclass
class Channel:
    name: str
    topic: str
    owner: str
    user_count: int
