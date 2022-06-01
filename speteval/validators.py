from typing import Set, Union
from .exceptions import FileNotExist, InvalidRange
from .interfaces import IValidator
from .constants import FilePath, AudioContent, ValidatorsNames
from .utils import (
    get_file_extension,
    get_max_dim,
    get_min_dim,
    get_text_to_frame_ratio,
    get_text_to_speech_ratio,
    load_audio
    )
import os


class FileExistanceVal(IValidator):
    """Validates whether the file is exist or not
    """
    name = ValidatorsNames.FileExistanceVal

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def validate(self, audio_path: FilePath, *args, **kwargs) -> bool:
        return os.path.exists(audio_path)


class LoadbilityVal(IValidator):
    """Validates whether the file is readable/corrupted or not
    """
    name = ValidatorsNames.LoadbilityVal

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def validate(self, audio_path: FilePath, *args, **kwargs) -> bool:
        try:
            _ = load_audio(audio_path)
        except FileNotExist as e:
            raise e
        except RuntimeError:
            return False
        except Exception as e:
            raise e
        return True


class ChannelsVal(IValidator):
    """Validates whether the number of channels of the audio
    is valid or not.

    Args:
        n_channels (int): The expected number of channels
        min_length (int): The min length of the audio content
        this is used when the array/Tensor passed in 1d (MONO), Default 100
    """
    name = ValidatorsNames.ChannelsVal

    def __init__(
            self, n_channels: int, min_length=100, *args, **kwargs
            ) -> None:
        self.n_channels = n_channels
        self.min_length = min_length

    def validate(self, content: AudioContent, *args, **kwargs) -> bool:
        min_dim = get_min_dim(content)
        if min_dim >= self.min_length:
            return self.n_channels == 1
        return len(content) == self.n_channels


class SampleRateVal(IValidator):
    """Validates whether the sampling rate of the audio
    is valid or not.

    Args:
        target_sr (int): The target sampling rate to copmare with.
    """
    name = ValidatorsNames.SampleRateVal

    def __init__(self, target_sr: int, *args, **kwargs) -> None:
        self.target_sr = target_sr

    def validate(self, loadded_sr: int, *args, **kwargs):
        return loadded_sr == self.target_sr


class ExtensionVal(IValidator):
    """Validates if the audio has a valid extenshion or not

    Args:
        valid_exts (Set[str]): The set of valid extensions without dot (i.e
        wav, mp3 ..etc)
    """
    name = ValidatorsNames.ExtensionVal

    def __init__(self, valid_exts: Set[str], *args, **kwargs) -> None:
        if isinstance(valid_exts, set) is False:
            self.valid_exts = set(valid_exts)
        else:
            self.valid_exts = valid_exts

    def validate(self, audio_path: FilePath, *args, **kwargs):
        ext = get_file_extension(audio_path)
        return ext in self.valid_exts


class TextToSpeechVal(IValidator):
    """Validates whether the text to speech ratio is within the valid
    range or not

    Args:
        min_ratio (float): The minimum value that the ratio of the
        text-to-speech ration should be higher than, the value should be
        between 0 and 1.
        max_ratio (float): The maximum value that the ratio of the
        text-to-speech ration should be less than, the value should be
        between 0 and 1.
    """
    _min_val = 0
    _max_val = 1
    name = ValidatorsNames.TextToSpeechVal

    def __init__(
            self, min_ratio: float, max_ratio: float, *args, **kwargs
            ) -> None:
        assert 0.0 <= min_ratio <= 1.0, InvalidRange(
            self._min_val, self._max_val, min_ratio
            )
        assert 0.0 <= max_ratio <= 1.0, InvalidRange(
            self._min_val, self._max_val, max_ratio
            )
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

    def validate(
            self, text: str, content: AudioContent, *args, **kwargs
            ) -> bool:
        return self.min_ratio <= get_text_to_speech_ratio(
            text, content
            ) <= self.max_ratio


class TextToFrameVal(IValidator):
    """Validates whether the text to frame ratio is within the valid
    range or not, this check is helpful for CTC loss which ensure the target
    text is less than or equal the numbre of frames.

    Args:
        hop_length (int): The featurizer hop length
        threshold (float): The maximum value that the text-to-speech
        ratio should be less than, the value should be
        between 0 and 1.
    """
    name = ValidatorsNames.TextToFrameVal

    def __init__(
            self, hop_length: int, threshold=1.0, *args, **kwargs
            ) -> None:
        super().__init__()
        self.hop_length = hop_length
        self.threshold = threshold

    def validate(
            self, text: str, content: AudioContent, *args, **kwargs
            ) -> bool:
        return 0 < get_text_to_frame_ratio(text, content) <= self.threshold


class LengthVal(IValidator):
    """Validates whether the text/speech length is within the valid range
    or not.

    Args:
        max_len (int): The maximum length that the input should be less than.
        min_len (int): The minimum length that the input should be
        greater than.
    """
    name = ValidatorsNames.LengthVal

    def __init__(
            self, max_len: int, min_len: int, *args, **kwargs
            ) -> None:
        self.min_len = min_len
        self.max_len = max_len

    def validate(
            self, content: Union[AudioContent, str], *args, **kwargs
            ) -> bool:
        if isinstance(content, str) is True:
            length = len(content)
        else:
            length = get_max_dim(content)
        return self.min_len <= length <= self.max_len
