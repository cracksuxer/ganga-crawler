from dataclasses import dataclass

@dataclass
class Add:
    title: str
    description: str
    price: float
    category: str
    image: str