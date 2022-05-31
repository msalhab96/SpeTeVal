from typing import Union


class FileNotExist(Exception):
    def __init__(self, file_path) -> None:
        msg = f"{file_path} does not exist!"
        super().__init__(msg)


class InvalidRange(Exception):
    def __init__(
            self,
            min_val: Union[int, float],
            max_val: Union[int, float],
            value: Union[int, float]
            ) -> None:
        msg = "Expected value with range ({}, {}), {} given"
        msg = msg.format(min_val, max_val, value)
        super().__init__(msg)
