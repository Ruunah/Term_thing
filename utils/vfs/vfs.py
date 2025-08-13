import os
import pathlib

class VFS:
    def __init__(self, root="~/.vfs_root"):
        self.root = pathlib.Path(root).expanduser()
        if not os.path.exists(self.root):
            self._initialize_root()

        self.home = self.root / "home"
        self.cwd = self.home
    
    def _initialize_root(self):
        os.makedirs(self.root, exist_ok=True)
        folders=["bin", "opt", "home", "tmp"]
        subfolders={"home":[".config", "Programs"]}

        for folder in folders:
            path=os.path.join(self.root, folder)
            os.makedirs(path, exist_ok=True)

        for key in subfolders:
            for folder in subfolders[key]:
                path=os.path.join(self.root, key, folder)
                os.makedirs(path, exist_ok=True)

def main():
    vfs = VFS()
    return vfs
