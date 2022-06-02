from abc import ABC, abstractmethod, abstractproperty


class IValidator(ABC):

    @abstractmethod
    def validate(self):
        pass

    @abstractproperty
    def name():
        pass


class IFilter(ABC):

    @abstractmethod
    def apply():
        pass

    @abstractmethod
    def apply_on_item():
        pass

    @abstractmethod
    def add_validator():
        pass

    @abstractmethod
    def remove_validator():
        pass
