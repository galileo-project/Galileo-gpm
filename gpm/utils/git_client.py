import os
from gitdb import GitDB
from git import Repo, Git
from github import Github, GithubObject
from gpm.utils.operation import LocalOperation
from gpm.utils.log import Log
from gpm.utils.console import gets
from gpm.const.status import Status

class GitClient(LocalOperation):
    _GITIGNORE_NAME = ".gitignore"

    def __init__(self, config = None):
        self._repo        = None
        self._origin      = None
        self._github      = None
        self._config      = config
        self.__uname      = None
        self.__password   = None
        self.__github_url = None

    @property
    def github_url(self):
        if not self.__github_url:
            self.__github_url = self._config.git_url or "git@github.com:%s/%s" % (self.user_account[0], self._config.name)
        return self.__github_url

    @property
    def user_account(self):
        self.__uname    = self.__uname or gets("Input GitHub user name")
        self.__password = self.__password or gets("Input GitHub password")
        return self.__uname, self.__password

    @property
    def github(self):
        if not self._github:
            self._github = GitHubClient(self.user_account[0], self.user_account[1])
        return self._github

    @property
    def repo(self):
        if not self._repo:
            self._repo = Repo(self.rel2abs(), odbt=GitDB)
        return self._repo

    @property
    def origin(self):
        if not self._origin:
            self._origin = self.repo.remotes[0]
        return self._origin

    def init(self, name = None, path = None):
        name  = name or self._config.name
        path  = path or self.rel2abs()
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

    def clone(self, url = None, to_path = None, branch = None):
        Log.info(Status["STAT_GET_PACKAGE"] % url)
        g = Git(to_path)
        g.clone(url or self.github_url)
        if branch:
            g.checkout(branch)
        return True

    def pull(self):
        self.origin.pull()

    def push(self):
        self.origin.push()

    def _add_remote(self, name, url):
        return self.repo.create_remote(name=name, url=url)

    def set_master_header(self):
        origin = self.repo.create_remote('origin', self.repo.remotes.origin.url)
        return self.repo.create_head("master", origin.refs.master).set_tracking_branch(origin.refs.master)

    def publish(self, name = "origin"):
        self._add_remote(name, self.github_url)
        self._create_remote(self._config.name, description = self._config.description or GithubObject.NotSet)
        self.set_master_header()
        self.push()

    def tag(self, path):
        return self.repo.tag(path)

    def _create_remote(self, name, *args, **kwargs):
        self.github.create_repo(name, *args, **kwargs)

    def create_gitignore(self):
        language = self._config.language
        if language:
            content = self.github.get_gitignore_template(language)
            LocalOperation.add_file(self._GITIGNORE_NAME, content)

    def safe_urljoin(self, *args):
        url = ""
        for section in args:
            section = section if section[-1] != "/" else section[:-1]
            url += section + "/"
        return url


##################################
#                                #
#          GitHub Client         #
#                                #
##################################

class GitHubClient(object):
    _API_GOOD = "good"

    def __init__(self, name, password):
        self.__username = name
        self.__password = password
        self._github = None
        self._user   = None

    def __verify_login(self, obj):
        if obj.get_api_status().status == self._API_GOOD:
            return True
        return False

    @property
    def user(self):
        if not self._user:
            self._user = self.github.get_user()
        return self._user

    @property
    def github(self):
        if not self._github:
            self._github = Github(self.__username, self.__password)
            if not self.__verify_login(self._github):
                Log.fatal(Status["STAT_LOGIN_GITHUB_FAILED"])
        return self._github

    def create_repo(self, name, *args, **kwargs):
        return self.user.create_repo(name=name, *args, **kwargs)

    def get_gitignore_template(self, name):
        return self.github.get_gitignore_template(name)
