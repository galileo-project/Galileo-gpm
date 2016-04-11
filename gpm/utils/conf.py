import yaml

class ConfReader:
    def __init__(self, path):
        self.path = path
        self.content = {}
        
    def read(self):
        with open(self.path, "r") as stream:
            self.content = yaml.load(stream)
        
    @property
    def author(self):
        return self.content.get("author")

    @property
    def description(self):
        return self.content.get("description")

    @property
    def version(self):
        return self.content.get("version")

    @property
    def email(self):
        return self.content.get("email")

    @property
    def language(self):
        return self.content.get("language")

    @property
    def build(self):
        return self.content.get("build")

    @property
    def install(self):
        return self.content.get("install")

    @property
    def test(self):
        return self.content.get("test")

    @property
    def dep(self):
        return self.content.get("dep")

    @property
    def name(self):
        return self.content.get("name")

    @property
    def git(self):
        return self.content.get("git")