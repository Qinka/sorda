import types

def function_wrap(cls):
    def wrap(*args, **kwargs):
        def real_wrap():
            cls(*args, **kwargs)
        return real_wrap
    return wrap


class Configurable:
    """Configurable

    """

    def __init__(self, ):
        """
        """
        self._meta = {}

    def registry(self, name: str, cls: type):
        """
        """
        if not hasattr(cls, 'meta_dict'):
            raise Exception("need `meta_dict' to parse")

        if isinstance(cls, types.FunctionType):
            self._meta[name] = function_wrap(cls)
        else:
            self._meta[name] = cls

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
