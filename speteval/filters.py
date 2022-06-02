from .constants import DataItem, FilePath, ValidatorsNames
from .interfaces import IFilter, IValidator
from pandarallel import pandarallel
from typing import List, Union
from pandas import DataFrame
from .utils import (
    export_csv,
    load_audio,
    load_csv
    )
import logging


class BaseFilter(IFilter):

    def __init__(self, validators: List[IValidator]) -> None:
        super().__init__()
        self.validators = {
            validator.name: validator for validator in validators
        }

    def add_validator(self, validator: IValidator) -> None:
        if validator.name in self.validators:
            msg = '{} already in the validators, {} updated!'
            logging.warning(
                msg.format(validator.name, validator.name)
            )
        self.validators[validator.name] = validator

    def remove_validator(self, validator: IValidator) -> None:
        self.validators.pop(validator.name)

    def apply(self, items: List[DataItem]):
        return list(filter(self.apply_on_item, items))

    def apply_on_item(self, item: DataItem, *args, **kwargs) -> bool:
        return self._filter(*item, *args, **kwargs)

    def _filter(self, audio_path, text, *args, **kwargs):
        if ValidatorsNames.LoadbilityVal in self.validators:
            if self.validators[ValidatorsNames.LoadbilityVal].validate(
                    audio_path=audio_path
                    ) is True:
                content = load_audio(audio_path=audio_path)
            else:
                return False
        for validator in self.validators:
            if validator.name == ValidatorsNames.LoadbilityVal:
                continue
            if validator.validate(
                    text=text,
                    audio_path=audio_path,
                    content=content,
                    *args,
                    **kwargs
                    ) is False:
                return False
        return True


class DataFrameFilter(BaseFilter):
    def __init__(
            self,
            validators: List[IValidator],
            path_key: str,
            text_key: str
            ) -> None:
        super().__init__(validators)
        self.path_key = path_key
        self.text_key = text_key

    def apply(self, df: DataFrame) -> DataFrame:
        msg = 'column "{}" not found in the given dataframe!'
        assert self.path_key in df.columns, KeyError(msg.format(self.path_key))
        assert self.text_key in df.columns, KeyError(msg.format(self.text_key))
        pandarallel.initialize()
        return df[df.parallel_apply(self.apply_on_item, axis=1)]

    def apply_on_item(self, item: DataItem, *args, **kwargs) -> bool:
        return self._filter(
            audio_path=item[self.path_key], text=self.path_key, *args, **kwargs
            )


class CSVFilter(DataFrameFilter):
    def __init__(
            self,
            validators: List[IValidator],
            path_key: str,
            text_key: str,
            *args,
            **kwargs
            ) -> None:
        super().__init__(validators, path_key, text_key)
        self._args = args
        self._kwargs = kwargs

    def apply(
            self,
            file_path: FilePath,
            return_df=False,
            save_to=None,
            *args,
            **kwargs
            ) -> Union[DataFrame, None]:
        df = load_csv(file_path, *self._args, **self._kwargs)
        if return_df is True:
            return super().apply(df, *args, **kwargs)
        assert save_to is not None, TypeError('save_to path is None!')
        export_csv(super().apply(df, *args, **kwargs), *args, **kwargs)
