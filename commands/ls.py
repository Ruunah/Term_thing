import os
import datetime
from pathlib import Path
def run(args=""):
    if not args:            
        current_dir='.'
    else:
        check=args[0]
        if "-"==check[0]:
            #check long args
            print("not implemented")
        del check
    files=[]
    dirs=[]
    items={}
    print("Mod_Time      Name")
    for item in Path(current_dir).iterdir():
        try:
            if item.is_dir():
                dirs+=str(item),''
            else:
                files+=str(item),''
            stats = os.stat(item)
            mod_time = str(datetime.datetime.fromtimestamp(stats.st_mtime)).split()
            items[str(item)]=(f"{mod_time[0]}    {item}")
        except FileNotFoundError:
            print(f"Error: {item} not found.")
    dirs=[item for item in dirs if item]
    dirs.sort()
    files=[item for item in files if item]
    files.sort()
    for i in range(len(dirs)):
        print(items[dirs[i]])
    for i in range(len(files)):
        print(items[files[i]])