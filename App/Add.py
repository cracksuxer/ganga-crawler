from dataclasses import dataclass
from box import Box

@dataclass
class Add:
    title: str
    img_link: str
    title_link: str
    img_title: str
    prices: Box
    location: str
    description: str
    labels: Box