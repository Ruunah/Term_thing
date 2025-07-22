import sys
import tomllib
from PySide4.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from PySide4.QtGui import QFontDatabase, QFont, QColor, QPalette
from PySide4.QtCore import Qt

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

defaults={
    "Window_dimensions":"800x600",
    "Fullscreen":"True",
    "Opacity":"0.85",

    "Font_family":"../fonts/JetBrainsMonoNerdFont-Medium.ttf",
    "Size":"14",

    "Background":"#011627",
    "Foreground":"#bdc1c6",
    "Bold":"#eeeeee",
    "Cursor":"#9ca1aa",
    "Cursor_Text":"#080808",
    "Selection":"#b2ceee",
    "Selection_Text":"#080808",
    "Black":"#1d3b53",
    "Red":"#fc514e",
    "Green":"#a1cd5e",
    "Yellow":"#e3d18a",
    "Blue":"#82aaff",
    "Purple":"#c792ea",
    "Cyan":"#7fdbca",
    "White":"#a1aab8",
    "Black_Bright":"#7c8f8f",
    "Red_Bright":"#ff5874",
    "Green_Bright":"#21c7a8",
    "Yellow_Bright":"#ecc48d",
    "Blue_Bright":"#82aaff",
    "Purple_Bright":"#ae81ff",
    "Cyan_Bright":"#7fdbca",
    "White_Bright":"#d6deeb",
}

def load_sets():
    failed_keys = []

    def safe_get(section, key):
        try:
            return config.get(section).get(key)
        except Exception as e:
            failed_keys.append(f"{section}.{key}: {str(e)}")
            return (defaults[key], "Default")
    # Window settings
    Dimensions      = safe_get("window", "Dimensions")
    Fullscreen      = safe_get("window", "Fullscreen")
    Opacity         = safe_get("window", "Opacity")
    # Font settings
    Font            = safe_get("font", "Font_Family")
    Font_size       = safe_get("font", "Size")
    # Color settings
    Background      = safe_get("colors", "Background")
    Foreground      = safe_get("colors", "Foreground")
    Bold            = safe_get("colors", "Bold")
    Cursor          = safe_get("colors", "Cursor")
    Cursor_Text     = safe_get("colors", "Cursor_Text")
    Selection       = safe_get("colors", "Selection")
    Selection_Text  = safe_get("colors", "Selection_Text")
    Black           = safe_get("colors", "Black")
    Red             = safe_get("colors", "Red")
    Green           = safe_get("colors", "Green")
    Yellow          = safe_get("colors", "Yellow")
    Blue            = safe_get("colors", "Blue")
    Purple          = safe_get("colors", "Purple")
    Cyan            = safe_get("colors", "Cyan")
    White           = safe_get("colors", "White")
    Black_Bright    = safe_get("colors", "Black_Bright")
    Red_Bright      = safe_get("colors", "Red_Bright")
    Green_Bright    = safe_get("colors", "Green_Bright")
    Yellow_Bright   = safe_get("colors", "Yellow_Bright")
    Blue_Bright     = safe_get("colors", "Blue_Bright")
    Purple_Bright   = safe_get("colors", "Purple_Bright")
    Cyan_Bright     = safe_get("colors", "Cyan_Bright")
    White_Bright    = safe_get("colors", "White_Bright")

    if failed_keys:
        print("Warning: Failed to load the following config keys:")
        for key in failed_keys:
            print(f"  - {key}")


def load_font():
    font_family = None

    if Font[1]:
        return Font = QFontDatabase.applicationFontFamilies(default_font_id = QFontDatabase.addApplicationFont(Font[0]))
    else:
        if Font.lower().endswith((".ttf", ".otf")) and os.path.isfile(Font):
            font_id = QFontDatabase.addApplicationFont(Font)
            if 0 > font_id:
                return (Font = QFontDatabase.applicationFontFamilies(default_font_id = QFontDatabase.addApplicationFont("../fonts/JetBrainsMonoNerdFont-Medium.ttf")), f"Error: Failed to load font at {Font}, using default.")
            else:
                family = QFontDatabase.applicationFontFamilies(font_id)
                if family:
                    return family[0]

        elif Font:
            if Font in QFontDatabase().families():
                return Font
            else:
                return (Font = QFontDatabase.applicationFontFamilies(default_font_id = QFontDatabase.addApplicationFont("../fonts/JetBrainsMonoNerdFont-Medium.ttf")), f"Warning: Font '{Font}' not found in system fonts, using default")


class TerminalWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.startup_messages = []
        self.initUI()

    def initUI(self):
        result = load_font()
        if isinstance(result, tuple):
            font_family, msg = result
            self.startup_messages.append(msg)
        else:
            font_family = result

        size_str = Font_size
        size_str = size_str.strip() if isinstance(size_str, str) else ""

        # Set font size
        try:
            size = int(size_str)
            if size <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            size = defaults[Font_size]
            self.startup_messages.append(f"\nWarning: value '{size_str}' not valid, using default")

        font = QFont(font_family, size)

        # Set Opacity
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()
        opacity_str = Opacity
        try:
            opacity=float(opacity_str)
        except (ValueError, TypeError):
            opacity = defaults[Opacity]
            self.startup_messages.append(f"\nWarning: value '{opacity_str}' not valid, using default")
        self.setWindowOpacity(opacity)
            
        self.setWindowOpacity()

        # Set Color palette
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#001120"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(font)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #001120;
                color: #037777777776ff00;
                caret-color: yellow;
            }
        """)
        self.text_edit.setCursorWidth(0)
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.setContentsMargins(-2, 0, 0, 0)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = TerminalWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()