from dataclasses import dataclass
from datetime import datetime

@dataclass
class Player:
    name: str
    rank: str
    join_date: datetime
    stars: int
    active: bool = True  # indica se o player ainda faz parte da aliança

    def __str__(self):
        status = "Active" if self.active else "Inactive"
        return f"{self.name} (Rank: {self.rank}, Joined: {self.join_date.strftime('%Y-%m-%d')}, Stars: {self.stars}, Status: {status})"


@dataclass
class PowerRegister:
    player: Player
    power_level: float
    date: datetime

    def __str__(self):
        return f"{self.player.name} - Power: {self.power_level} on {self.date.strftime('%Y-%m-%d')}"
