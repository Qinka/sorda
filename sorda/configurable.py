
import types
from typing import Tuple

class Configurable:
    """Configurable

    """

    def __init__(self, key: str = 'meta', attr: str = 'meta_dict', raw_config: Tuple[str, str] = ('sorda_raw_config', '_raw_config')):
        """
        """
        self._key  = key
        self._attr = attr

        self._raw_config_attr = raw_config[0]
        self._raw_config_arg  = raw_config[1]

        self._meta = {}
        self._type = {}

    def registry(self, *args: Tuple[str, type]):
        """
        """

        if len(args) == 1 and isinstance(args[0], str):
            name = args[0]
            def registry_wrap(cls: type):
                if not hasattr(cls, self._attr):
                    raise Exception(f"need `{self._attr}' to parse")

                self._meta[name] = cls
                self._type[name] = isinstance(cls, types.FunctionType)
                return cls
            return registry_wrap

        elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], (type, types.FunctionType)):
            name, cls = args
            if not hasattr(cls, self._attr):
                raise Exception(f"need `{self._attr}' to parse")

            self._meta[name] = cls
            self._type[name] = isinstance(cls, types.FunctionType)
        else:
            raise TypeError("registry need name or a name with class")

    def __call__(self, config: dict, ):
        """
        """
        if self._key not in config:
            raise Exception(f"need `{self._key}` to select")

        cls = self._meta[config[self._key]]
        meta_dict: dict = getattr(cls, self._attr)
        parameters = {}
        for key in meta_dict.keys():
            if meta_dict[key] in config:
                parameters[key] = config[meta_dict[key]]
            else:
                print('Warn unknow parameter:', key)

        if hasattr(cls, self._raw_config_attr) and getattr(cls, self._raw_config_attr):
            parameters[self._raw_config_arg] = config

        if self.is_func(config[self._key]):
            def func():
                return cls(**parameters)
            return func
        else:
            return cls(**parameters)

        return cls(**parameters), self.is_func(config['meta'])

    def is_func(self, key):
        return self._type[key]
