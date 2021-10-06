
from abc import ABCMeta, abstractmethod
from typing import Tuple, overload
from functools import reduce


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

class MetaGrid(metaclass = ABCMeta):
    @abstractmethod
    def step(self):
        raise NotImplementedError()

    @abstractmethod
    def __len__(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def value(self):
        raise NotImplementedError()

class GridRange(MetaGrid):
    def __init__(self, start: int, stop: int, step: int = None):
        if step is None:
            self._range = list(range(start, stop))
        else:
            self._range = list(range(start, stop, step))

        self._count = 0
        self._limit = len(self._range)

    def step(self):
        self._count = (self._count + 1) % self._limit

    def __len__(self):
        return self._limit

    @property
    def value(self):
        return self._range[self._count]

class GridEnum(MetaGrid):
    def __init__(self, items):
        self._items = items
        self._count = 0
        self._limit = len(items)

    def step(self):
        self._count = (self._count + 1) % self._limit

    def __len__(self):
        return self._limit

    @property
    def value(self):
        return self._items[self._count]

class GridExp(MetaGrid):
    def __init__(self, init: float, step: float, n: int):
        self._count = 0
        self._limit = n
        self._init  = init
        self._value = init
        self._step  = step

    def step(self):
        self._count += 1
        if self._count < self._limit:
            self._value *= self._step
        else:
            self._count = 0
            self._value = self._init

    def __len__(self):
        return self._limit

    @property
    def value(self):
        return self._value


class GridSearch(UpdaterBase):

    meta_dict = {
        'update': 'update'
    }

    @staticmethod
    def recursive_update_split(up: dict) -> Tuple[dict, dict, list]:
        s = {}
        d = {}
        n = []

        for k in up:
            if isinstance(up[k], dict):
                if 'meta' in up[k]:
                    cfg = up[k]
                    # grid search updater
                    if cfg['meta'] == 'range':
                        grid = GridRange(start = cfg['start'], stop = cfg['stop'], step = cfg.get('step', None))
                    elif cfg['meta'] == 'exp':
                        grid = GridExp(cfg['init'], cfg['step'], cfg['n'])
                    elif cfg['meta'] == 'items':
                        grid = GridEnum(cfg['items'])
                    n.append(grid)
                    d[k] = grid
                else:
                    _s, _d, _n = GridSearch.recursive_update_split(up[k])
                    if len(_s) > 0:
                        s[k] = _s
                    if len(_d) > 0:
                        d[k] = _d
                    if len(_n) > 0:
                        n.extend(_n)
            else:
                s[k] = up[k]
        return s, d, n

    @staticmethod
    def config_replace(config: dict, update: dict):
        for p in update:
            if p in config:
                if isinstance(update[p], dict) and isinstance(config[p], dict):
                    GridSearch.config_replace(config[p], update[p])
                elif isinstance(update[p], MetaGrid):
                    config[p] = update[p].value
                else:
                    config[p] = update[p]
            else:
                print("warning", "unhandled key", p, 'in config', config)


    def __init__(self, update: dict):
        self._config = None
        self._update_static, self._update_dynamic, self._grids \
            = GridSearch.recursive_update_split(update)
        self._limits = [len(g) for g in self._grids]
        self._limit = reduce(lambda x, y: x * y, self._limits, 1)
        self._count = 0
        self._counts = [0] * len(self._limits)

    def load_origin(self, cfg: dict):
        self._config = cfg.copy()
        GridSearch.config_replace(self._config, self._update_static)

    # def reset(self, ):
    #     self._config = {}
    #     self._n = 0

    # def update(self, _results):
    #     return

    def __iter__(self):
        return self

    def step(self):
        for i in range(len(self._counts)):
            self._counts[i] += 1
            self._grids[i].step()
            if self._counts[i] < self._limits[i]:
                break
            else:
                self._counts[i] = 0
                continue

    def __next__(self):
        if self._count < self._limit:
            self._count += 1
            config = self._config.copy()
            GridSearch.config_replace(config, self._update_dynamic)
            self.step()
            return config
        else:
            raise StopIteration
