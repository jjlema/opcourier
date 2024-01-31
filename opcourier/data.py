from marshmallow_dataclass import dataclass
from typing import Tuple, List


@dataclass
class KnapsackData:
    items: List[Tuple[int, int, int]]
    capacity: int


@dataclass
class KnapsackResult:
    items: List[int]
    usedCapacity: int
    profit: int
    solved: bool
    time: float

    


data = KnapsackData(items=[(1, 10, 20), (2, 5, 28), (3, 2, 17), (4, 5, 38), (5, 4, 38)], capacity=10)
print(data)