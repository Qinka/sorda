
import types
from typing import Tuple

class Configurable:
    """Configurable

    """

    def __init__(self, ):
        """
        """
        self._meta = {}
        self._type = {}

    def registry(self, name: str, cls: type):
        """
        """
        if not hasattr(cls, 'meta_dict'):
            raise Exception("need `meta_dict' to parse")

        self._meta[name] = cls
        self._type[name] = isinstance(cls, types.FunctionType)

    def registry_(self, *args: Tuple[str, type]):
        """
        """

        if len(args) == 1 and isinstance(args[0], str):
            name = args[0]
            def registry_wrap(cls: type):
                if not hasattr(cls, 'meta_dict'):
                    raise Exception("need `meta_dict' to parse")

                self._meta[name] = cls
                self._type[name] = isinstance(cls, types.FunctionType)
                return cls
            return registry_wrap

        elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], (type, types.FunctionType)):
            name, cls = args
            if not hasattr(cls, 'meta_dict'):
                raise Exception("need `meta_dict' to parse")

            self._meta[name] = cls
            self._type[name] = isinstance(cls, types.FunctionType)
        else:
            raise TypeError("registry need name or a name with class")

    def __call__(self, config: dict):
        """
        """
        if 'meta' not in config:
            raise Exception("need meta to select")

        cls = self._meta[config['meta']]
        meta_dict: dict = cls.meta_dict
        parameters = {}
        for key in meta_dict.keys():
            if meta_dict[key] in config:
                parameters[key] = config[meta_dict[key]]
        return cls(**parameters), self.is_func(config['meta'])

    def is_func(self, key):
        return self._type[key]
