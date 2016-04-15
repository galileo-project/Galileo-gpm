from gpm.utils.operation import LocalOperation
from gpm.const import GPM_DB, DB_SF
import os
try:
    import cPickle as pickle
except:
    import pickle

class StaticDB(object):
    def __init__(self):
        self.__path = os.path.join(GPM_DB, "%s.%s" % (self.__class__.__name__, DB_SF))
        self.__data = {}
        self.__load()

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __delattr__(self, item):
        self.__delitem__(item)

    def __getitem__(self, item):
        return self.__data.get(item)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self.__data[key]

    def __del__(self):
        self.__save()

    def __len__(self):
        return len(self.__data)

    def update(self, data):
        self.add(data)

    def add(self, data):
        if self.__file_exist:
            self.__load()

        self.__data.update(data)
        self.__save()

    def __save(self, data = None):
        with open(self.__path, "wb") as stream:
            pickle.dump(data or self._data, stream)
        self._data = data

    def __load(self):
        if self.__file_exist:
            with open(self.__path, "rb") as stream:
                data = pickle.load(stream)
            self._data =  data or {}

    @property
    def __file_exist(self):
        db_dir = os.path.dirname(self.__path)
        if not LocalOperation.exist(db_dir):
            LocalOperation.mkdir(db_dir)
        return LocalOperation.exist(self.__path)