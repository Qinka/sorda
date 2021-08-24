
import types

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
        return cls(**parameters)

    def is_func(self, key):
        return self._type(key)
