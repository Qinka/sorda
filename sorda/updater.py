
from abc import ABCMeta, abstractmethod

class UpdaterBase(metaclass = ABCMeta):

    # @abstractmethod
    # def parse_base_configure(self, cfg: dict):
    #     pass
    # @abstractmethod
    # def parse_update_configure(self, cfg: dict):
    #     pass

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def load_origin(self, cfg: dict):
        pass

    @abstractmethod
    def __iter__(self):
        pass
    @abstractmethod
    def __next__(self):
        pass
    # @abstractmethod
    # def reset(self):
    #     pass
    # @abstractmethod
    # def update(self, results: dict):
    #     pass