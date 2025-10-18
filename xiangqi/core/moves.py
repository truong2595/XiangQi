#Hàm định nghĩa lớp Move đại diện cho nước đi
from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class Move:
    from_file: int
    from_rank: int
    to_file: int
    to_rank: int
    captured_id: Optional[int] = None

    def key(self) -> tuple[int,int,int,int]:
        return (self.from_file, self.from_rank, self.to_file, self.to_rank)

    def __repr__(self) -> str:
        return f"Move(({self.from_file},{self.from_rank})->({self.to_file},{self.to_rank}), cap={self.captured_id})"