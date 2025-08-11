from utils import module_registry, module_dir_registry

if __name__ == "__main__":
    vfs = module_registry["vfs.vfs"]()
    module_registry["window.window"](vfs)
