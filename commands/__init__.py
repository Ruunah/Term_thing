import os
import importlib

# Command storage dictionary
command_registry={}

for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename!="__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(f"commands.{module_name}")

        if hasattr(module, "run"):
            command_registry[module_name] = module.run
