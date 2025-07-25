import os
import sys
import importlib

module_dir_registry = {}
module_registry = {}

base_path = os.path.dirname(__file__)
package_root = "utils"
sys.path.append(os.path.abspath(os.path.join(base_path, "..")))

for root, dirs, files in os.walk(base_path):
    for filename in files:
        if filename.endswith(".py") and filename != "__init__.py":
            rel_path = os.path.relpath(os.path.join(root, filename), base_path)
            dotted_path = rel_path.replace(os.path.sep, ".")[:-3]
            full_module_name = f"{package_root}.{dotted_path}"

            try:
                module = importlib.import_module(full_module_name)
                if hasattr(module, "main"):
                    module_registry[dotted_path] = module.main
            except Exception as e:
                print(f"Failed to load {full_module_name}: {e}")

for name in os.listdir(base_path):
    if os.path.isdir(os.path.join(base_path, name)) and name != "__pycache__":
        module_dir_registry[name] = []

for name in os.listdir(base_path):
    for other in module_registry:
        if name != other and other.startswith(name + "."):
            module_dir_registry[name].append(module_registry[other])
