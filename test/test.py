import pkgutil
import sys

class Test:
    def run(self):
        """
        for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
            mod = loader.find_module(module_name).load_module(module_name)
            try:
                cls = mod._Test
                cls.run()
            except:
                print("Error: ", module_name)
                sys.exit(1)
        """
        print("test mod")
        sys.exit(0)


if __name__ == "__main__":
    Test().run()