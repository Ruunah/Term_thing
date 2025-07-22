import sys
import tomllib
from PySide4.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from PySide4.QtGui import QFontDatabase, QFont, QColor, QPalette
from PySide4.QtCore import Qt

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

defaults={
    "Window_dimensions":"800x600"
    "Fullscreen":"True"
    "Opacity":"0.85"

    "Font":"../fonts/JetBrainsMonoNerdFont-Medium.ttf",
    "FSize":"14",

    "Background":"#011627"
    "Foreground":"#bdc1c6"
    "Bold":"#eeeeee"
    "Cursor":"#9ca1aa"
    "Cursor_Text":"#080808"
    "Selection":"#b2ceee"
    "Selection_Text":"#080808"
    "Black":"#1d3b53"
    "Red":"#fc514e"
    "Green":"#a1cd5e"
    "Yellow":"#e3d18a"
    "Blue":"#82aaff"
    "Purple":"#c792ea"
    "Cyan":"#7fdbca"
    "White":"#a1aab8"
    "Black_Bright":"#7c8f8f"
    "Red_Bright":"#ff5874"
    "Green_Bright":"#21c7a8"
    "Yellow_Bright":"#ecc48d"
    "Blue_Bright":"#82aaff"
    "Purple_Bright":"#ae81ff"
    "Cyan_Bright":"#7fdbca"
    "White_Bright":"#d6deeb"
}

def load_sets():
    try:
        Dimensions     = config.get("window").get("Dimensions")
        Fullscreen     = config.get("window").get("Fullscreen")
        Opacity        = config.get("window").get("Opacity")

        Font           = config.get("font").get("Font_Family")
        Font_size      = config.get("font").get("Size")

        Background     = config.get("colors").get("Background")
        Foreground     = config.get("colors").get("Foreground")
        Bold           = config.get("colors").get("Bold")
        Cursor         = config.get("colors").get("Cursor")
        Cursor_Text    = config.get("colors").get("Cursor_Text")
        Selection      = config.get("colors").get("Selection")
        Selection_Text = config.get("colors").get("Selection_Text")
        Black          = config.get("colors").get("Black")
        Red            = config.get("colors").get("Red")
        Green          = config.get("colors").get("Green")
        Yellow         = config.get("colors").get("Yellow")
        Blue           = config.get("colors").get("Blue")
        Purple         = config.get("colors").get("Purple")
        Cyan           = config.get("colors").get("Cyan")
        White          = config.get("colors").get("White")
        Black_Bright   = config.get("colors").get("Black_Bright")
        Red_Bright     = config.get("colors").get("Red_Bright")
        Green_Bright   = config.get("colors").get("Green_Bright")
        Yellow_Bright  = config.get("colors").get("Yellow_Bright")
        Blue_Bright    = config.get("colors").get("Blue_Bright")
        Purple_Bright  = config.get("colors").get("Purple_Bright")
        Cyan_Bright    = config.get("colors").get("Cyan_Bright")
        White_Bright   = config.get("colors").get("White_Bright")

def load_font():
    font_family = None
    font_path = config.get("font", {}).get("Font_family", "").strip()
    default_font_id = QFontDatabase.addApplicationFont("../fonts/JetBrainsMonoNerdFont-Medium.ttf")
    default_family = QFontDatabase.applicationFontFamilies(default_font_id)

    if font_path.lower().endswith((".ttf", ".otf")) and os.path.isfile(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if 0 > font_id:
            return (default_family[0], f"Error: Failed to load font at {font_path}, using default.")
        else:
            family = QFontDatabase.applicationFontFamilies(font_id)
            if family:
                return family[0]

    elif font_path:
        if font_path in QFontDatabase().families():
            return font_path
        else:
            return (default_family[0], f"Warning: Font '{font_path}' not found in system fonts, using default")

    else:
        return default_family[0]

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

        size_str = config.get("font", {}).get("Size", "")
        size_str = size_str.strip() if isinstance(size_str, str) else ""


        try:
            size = int(size_str)
            if size <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            size = 14
            self.startup_messages.append(f"\nWarning: value '{size_str}' not valid, using default")


        font = QFont(font_family, size)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()
        opacity_str = config.get("window settings", {}).get("opacity", "")
        try:
            opacity=float(opacity_str)
        except (ValueError, TypeError):
            opacity = 0.85
            self.startup_messages.append(f"\nWarning: value '{opacity}' not valid, using default")
        self.setWindowOpacity(opacity)
            
        self.setWindowOpacity()

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