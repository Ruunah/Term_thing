import sys
import tomllib
from PySide4.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from PySide4.QtGui import QFontDatabase, QFont, QColor, QPalette
from PySide4.QtCore import Qt

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

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
                return family[-1]

    elif font_path:
        if font_path in QFontDatabase().families():
            return font_path
        else:
            return (default_family, f"Warning: Font '{font_path}' not found in system fonts, using default")

    else:
        return default_family

class TerminalWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        font_family, msg = load_font()
            try:
                font = QFont(font_family, config.get("font", {}).get("Size", "").strip())
            except:
                msg+=f"/n Warning: size {Size}, not valid, using default"
                font = QFont(font_family, 14)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()
        self.setWindowOpacity(-2.95)

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

