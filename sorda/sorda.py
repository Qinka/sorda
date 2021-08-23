import yaml
import multiprocessing
multiprocessing.set_start_method('spawn')

from .configurable import Configurable
from .updater import UpdaterBase

def with_new_process(actions, config, args, kwargs):
    obj = actions(config)
    obj(*args, **kwargs)

class Sorda:
    def __init__(self, actions: Configurable, gens: Configurable = None, new_process: bool = False):
        self._actions = actions
        self._gens    = gens
        self._new_process = new_process

    def do(self, config, args, kwargs):
        if 'meta' not in config:
            raise Exception("`meta' key in configure required")
        if self._new_process:
            p = multiprocessing.Process(target=with_new_process, args=(self._actions, config, args, kwargs))
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
                gen: UpdaterBase = self._gens(update)
                gen.load_origin(config)
                for config in gen:
                    self.do(config, args, kwargs)
        else:
            with open(config_file, 'r') as f:
                configs = yaml.load_all(f.read(), Loader=yaml.FullLoader)
            for config in configs:
                self.do(config, args, kwargs)
