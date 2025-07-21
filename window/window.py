import sys
import tomllib
from PySide6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from PySide6.QtGui import QFontDatabase, QFont, QColor, QPalette
from PySide6.QtCore import Qt

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

class TerminalWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Load custom font (adjust path as needed)
        font_id = QFontDatabase.addApplicationFont("path/to/your/font.ttf")
        if font_id == -1:
            print("Failed to load font, using default.")
            font_family = "Courier New"
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        font = QFont(font_family, 12)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()
        self.setWindowOpacity(0.95)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#001122"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(font)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #001122;
                color: #00ff00;
                caret-color: yellow;
            }
        """)
        self.text_edit.setCursorWidth(2)
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = TerminalWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

