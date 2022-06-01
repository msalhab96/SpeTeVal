from abc import ABC, abstractmethod, abstractproperty


class IValidator(ABC):

    @abstractmethod
    def validate(self):
        pass

    @abstractproperty
    def name():
        pass
