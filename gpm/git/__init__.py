import os
from gitdb import GitDB
from git import Repo
from gpm.utils.operation import LocalOperation

class GitClient(LocalOperation):
    def __init__(self):
        self._repo   = None
        self._origin = None

    @property
    def repo(self):
        if not self._repo:
            self._repo  =Repo(self.rel2abs(), odbt=GitDB)
        return self._repo

    @property
    def origin(self):
        if not self._origin:
            self._origin = self.repo.remotes.origin
        return self._origin

    def init(self, name, path = None):
        path = path or self.rel2abs()
        repo_path = os.path.join(path, name)
        repo = Repo.init(repo_path, odbt=GitDB)
        self._repo = repo
        return repo.bare

    def add(self, paths):
        _paths = []
        if not isinstance(paths, list):
            paths = [paths]
        for path in paths:
            _paths.append(self.rel2abs(path))
        return self.repo.index.add(_paths)

    def commit(self, msg):
        return self.repo.index.commit(msg)

    def clone(self, path):
        self.repo.clone(path)

    def pull(self):
        self.origin.pull()

    def push(self):
        self.origin.push()

    def publish(self, name, url):
        return self.repo.create_remote(name=name, url=url)

    def tag(self, path):
        self.repo.tag(path)