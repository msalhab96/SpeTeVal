from typing import Callable, List, Tuple, Union
from .constants import FilePath, AudioContent
from .decorators import check_file_existance
from pandas import DataFrame
from torch import Tensor
import pandas as pd
import numpy as np
import torchaudio
import os


@check_file_existance
def load_audio(audio_path: FilePath) -> Tuple[Tensor, int]:
    x, sr = torchaudio.load(audio_path, channels_first=True)
    return x, sr


def _get_dim(content: AudioContent, operation: Callable) -> int:
    length = len(content)
    while True:
        try:
            content = content[0]
            length = operation(length, len(content))
        except Exception:
            break
    return length


def get_min_dim(content: AudioContent) -> int:
    return _get_dim(content, min)


def get_max_dim(content: AudioContent) -> int:
    return _get_dim(content, max)


def get_file_extension(file_path: FilePath) -> str:
    return os.path.splitext(file_path)[-1].replace('.', '')


def get_text_to_speech_ratio(
        text: str, content: AudioContent, eps=1e-9
        ) -> float:
    max_dim = max(get_max_dim(content), eps)
    return len(text) / max_dim


def get_n_frames(content: AudioContent, hop_length: int) -> int:
    n_samples = get_max_dim(content)
    hop_length = max(1, hop_length)
    return int(n_samples) // hop_length


def get_text_to_frame_ratio(
        text: str, content: AudioContent, hop_length: int, eps=1e-9
        ) -> float:

    return len(text) / max(eps, get_n_frames(content, hop_length))


def get_std(values: List[Union[float, int]]) -> float:
    return np.std(values)


def get_mean(values: List[Union[float, int]]) -> float:
    return np.mean(values)


def load_csv(file_path: FilePath, *args, **kwargs) -> DataFrame:
    return pd.read_csv(file_path, *args, **kwargs)


def export_csv(df: DataFrame, file_path: FilePath, *args, **kwargs) -> None:
    df.to_csv(file_path, *args, **kwargs)
