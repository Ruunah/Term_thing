import os
import pathlib

class VFS:
    def __init__(self, root="~/.vfs_root"):
        self.root = os.path.expanduser(root)
        if not os.path.exists(self.root):
            self._initialize_root()
    
    def _initialize_root(self):
        os.makedirs(self.root, exist_ok=True)
        folders=["bin", "opt", "etc", "home", "media", "tmp", "usr", "var"]
        subfolders={
                "usr":["bin", "include", "lib", "sbin"],
                "var":["cache", "log", "spool", "tmp"],
                }

        for folder in folders:
            path=os.path.join(self.root, folder)
            os.makedirs(path, exist_ok=True)

        for key in subfolders:
            for folder in subfolders[key]:
                path=os.path.join(self.root, key, folder)
                os.makedirs(path, exist_ok=True)
def main():
    vfs = VFS()

if __name__ == "__main__":
    main()
