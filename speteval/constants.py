from dataclasses import dataclass
from typing import (
    Tuple,
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
DataItem = List[Tuple[FilePath, str]]


@dataclass
class ValidatorsNames:
    FileExistanceVal = 'FileExistanceVal'
    LoadbilityVal = 'LoadbilityVal'
    ChannelsVal = 'ChannelsVal'
    SampleRateVal = 'SampleRateVal'
    ExtensionVal = 'ExtensionVal'
    TextToSpeechVal = 'TextToSpeechVal'
    TextToFrameVal = 'TextToFrameVal'
    LengthVal = 'LengthVal'
