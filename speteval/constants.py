from typing import (
    Union,
    List
)
from torch import Tensor
from numpy import ndarray
from pathlib import Path


Sample = Union[float, int]
Mono = List[Sample]
Sterio = Union[List[List[Sample]], List[Sample]]
FilePath = Union[Path, str]
AudioContent = Union[
    Tensor,
    Mono,
    Sterio,
    ndarray
]
