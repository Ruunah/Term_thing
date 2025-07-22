import sys
import tomllib
from PySide6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from PySide6.QtGui import QFontDatabase, QFont, QColor, QPalette
from PySide6.QtCore import Qt

# Imports Settings from config.toml
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# Loads defaults outide of user space because I dont trust myself, imagine users
defaults={

    # Window settings
    "Dimensions"      : "800x600",
    "Fullscreen"      : "True",
    "Frame"           : "False",
    "Opacity"         : "0.85",

    # Font and font size
    "Font_family"     : "../fonts/JetBrainsMonoNerdFont-Medium.ttf",
    "Size"            : "14",

    # Colorscheme
    "Frame_color"     : "Transparent",
    "Background"      : "#011627",
    "Foreground"      : "#bdc1c6",
    "Bold"            : "#eeeeee",
    "Cursor"          : "#9ca1aa",
    "Cursor_Text"     : "#080808",
    "Selection"       : "#b2ceee",
    "Selection_Text"  : "#080808",
    "Black"           : "#1d3b53",
    "Red"             : "#fc514e",
    "Green"           : "#a1cd5e",
    "Yellow"          : "#e3d18a",
    "Blue"            : "#82aaff",
    "Purple"          : "#c792ea",
    "Cyan"            : "#7fdbca",
    "White"           : "#a1aab8",
    "Black_Bright"    : "#7c8f8f",
    "Red_Bright"      : "#ff5874",
    "Green_Bright"    : "#21c7a8",
    "Yellow_Bright"   : "#ecc48d",
    "Blue_Bright"     : "#82aaff",
    "Purple_Bright"   : "#ae81ff",
    "Cyan_Bright"     : "#7fdbca",
    "White_Bright"    : "#d6deeb",
}

# User settings
def load_sets():
    failed=[]

    # Function to solve errors from user settings
    def safe_get(section, key):
        try:
            return config.get(section).get(key)

        except Exception as e:
            failed.append(f"{selection}.{key}")
            return(defaults[key])
    
    # Importing sets
    sets={

        # Window settings
        "Dimensions"      : safe_get("window", "Dimensions"),
        "Fullscreen"      : safe_get("window", "Fullscreen"),
        "Frame"           : safe_get("window", "Frame"),
        "Opacity"         : safe_get("window", "Opacity"),

        # Font and Font size
        "Font_family"     : safe_get("font", "Font_family"),
        "Font_size"       : safe_get("font", "Size"),

        # Colorscheme
        "Frame_color"     : safe_get("colors", "Frame_color"),
        "Background"      : safe_get("colors", "Background"),
        "Foreground"      : safe_get("colors", "Foreground"),
        "Bold"            : safe_get("colors", "Bold"),
        "Cursor"          : safe_get("colors", "Cursor"),
        "Cursor_Text"     : safe_get("colors", "Cursor_Text"),
        "Selection"       : safe_get("colors", "Selection"),
        "Selection_Text"  : safe_get("colors", "Selection_Text"),
        "Black"           : safe_get("colors", "Black"),
        "Red"             : safe_get("colors", "Red"),
        "Green"           : safe_get("colors", "Green"),
        "Yellow"          : safe_get("colors", "Yellow"),
        "Blue"            : safe_get("colors", "Blue"),
        "Purple"          : safe_get("colors", "Purple"),
        "Cyan"            : safe_get("colors", "Cyan"),
        "White"           : safe_get("colors", "White"),
        "Black_Bright"    : safe_get("colors", "Black_Bright"),
        "Red_Bright"      : safe_get("colors", "Red_Bright"),
        "Green_Bright"    : safe_get("colors", "Green_Bright"),
        "Yellow_Bright"   : safe_get("colors", "Yellow_Bright"),
        "Blue_Bright"     : safe_get("colors", "Blue_Bright"),
        "Purple_Bright"   : safe_get("colors", "Purple_Bright"),
        "Cyan_Bright"     : safe_get("colors", "Cyan_Bright"),
        "White_Bright"    : safe_get("colors", "White_Bright"),
    }

    if failed:
        fails=["Warning: Failed to load the following config keys: "]
        keys=[]
        for i in range(len(failed)):
            keys+=failed[i]
        fails+=keys
        return (sets, fails)

    else:
        return sets

# Font loader, bc its loang and I dont want it in the middle of the code
def load_font(defaults, sets, fails=[]):

    # Error just defaults so its easyer
    if len(fails) > 1 and f"font.{sets[Font_family]}" in fails[1]:
        return QFontDatabase.applicationFontFamilies(default_font_id = QFontDatabase.addApplicationFont(defaults[Font_family]))

    else:
        if sets[Font_family].lower().endswith((".ttf", ".otf")) and os.path.isfile(sets[Font_family]):
            font_id = QFontDatabase.addApplicationFont(sets[Font_family])
            if 0 > font_id:
                return QFontDatabase.applicationFontFamilies(default_font_id = QFontDatabase.addApplicationFont(defaults[Font_family]))

            else:
                family = QFontDatabase.applicationFontFamilies(font_id)
                if family:
                    return family[0]

                else:
                    return QFontDatabase.applicationFontFamilies(default_font_id = QFontDatabase.addApplicationFont(defaults[Font_family]))

        elif sets[Font_family]:
            if sets[Font_family] in QFontDatabase().families():
                return sets[Font_family]

            else:
                    return QFontDatabase.applicationFontFamilies(default_font_id = QFontDatabase.addApplicationFont(defaults[Font_family]))

class TerminalWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.startup_messages = []
        self.initUI()

    def initUI(self):
        result = load_sets()
        if isinstance(result, tuple):
            sets, msg = result
            fails = msg[1:]
            self.startup_messages.append(msg[0])

        else:
            sets = result

        ## Window
        # Fullscreen or Dimensions
        if isinstance(sets[Fullscreen], bool):
            if sets[Fullscreen]==True:
                self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
                self.showFullScreen()

            else:
                if not sets[Frame]:
                    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)



        ## Font
        # Font Size
        try:
            sets[Font_size] = int(sets[Font_size])
            if sets[Font_size] <= 0:
                raise ValueError()

        except (ValueError, TypeError):
            self.startup_messages.append(f"\nWarning: value 'sets[Font_size]' not valid, using default")
            sets[Font_size] = defaults[Font_size]

        # Get font
        sets[Font_family] = load_fonts()

        # Actually set the font
        font = QFont(sets[Font_family], sets[Font_size])
