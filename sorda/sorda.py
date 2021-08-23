import yaml
import multiprocessing

from .configurable import Configurable
from .updater import UpdaterBase

class Sorda:
    def __init__(self, actions: Configurable, gens: Configurable = None, multi_process: bool = False):
        self._actions = actions
        self._gens    = gens
        self._multi_process = multi_process

    def do(self, config, args, kwargs):
        if 'meta' not in config:
            raise Exception("`meta' key in configure required")
        if self._multi_process:
            p = multiprocessing.Process(target=self._actions(config, args=args, kwargs=kwargs))
            print('config', config)
            p.start()
            p.join()
        else:
            self._actions(config)(*args, **kwargs)

    def __call__(self, config_file, update_file = None, *args, **kwargs):

        if update_file is not None and self._gens is not None:
            with open(config_file, 'r') as f:
                config = yaml.load(f.read(), Loader=yaml.FullLoader)
            with open(update_file, 'r') as f:
                updates = yaml.load_all(f.read(), Loader=yaml.FullLoader)
            for update in updates:
                gen: UpdaterBase = self._gen(update)
                gen.load_origin(config)
                for config in gen:
                    self.do(config, args, kwargs)
        else:
            with open(config_file, 'r') as f:
                configs = yaml.load_all(f.read(), Loader=yaml.FullLoader)
            for config in configs:
                self.do(config, args, kwargs)
