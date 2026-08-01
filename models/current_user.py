from dataclasses import dataclass

@dataclass
class CurrentUser:
    id: int
    username: str
    full_name: str
    role: str