import re
import os
import sys
import tomllib
from PySide6.QtCore import Qt
from utils.window.QTermEdit import QTermEdit
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from utils.window.loads import defaults, load_sets, load_font, load_color

sets = load_sets(defaults)

class TerminalWindow(QWidget):
    def __init__(self, vfs):
        super().__init__()
        self.vfs = vfs
        self.startup_messages = []
        self.initUI()

    def initUI(self):
        self.term_edit = QTermEdit(self)
        result = load_sets()
        if isinstance(result, tuple):
            sets, msg = result
            fails = msg[1:]
            self.startup_messages.append(msg[0])

        else:
            fails=[]
            sets = result

        ## Window
        # Fullscreen or Dimensions
        if str(sets["Fullscreen"]).lower() == "true":
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.showFullScreen()

        else:
            if not sets["Frame"]:
                self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

            else:
                self.setWindowFlags(Qt.WindowType.Window)
                self.setWindowTitle(sets["Title"])

            if len(str(sets["Dimensions"]).split("x")) == 2:
                try:
                    width, height = sets["Dimensions"].split("x")
                    self.resize(int(width), int(height))
                except ValueError:
                    pass

        try:
            self.setWindowOpacity(float(sets["Opacity"]))
        except (ValueError, TypeError):
            self.setWindowOpacity(float(defaults["Opacity"]))

        ## Font
        # Font Size
        try:
            sets["Font_size"] = int(sets["Font_size"])
            if sets["Font_size"] <= 0:
                raise ValueError()

        except (ValueError, TypeError):
            self.startup_messages.append(f"\nWarning: value '{sets['Font_size']}' not valid, using default")
            sets["Font_size"] = defaults["Font_size"]

        # Get font
        sets["Font_family"] = load_font(defaults, sets, fails)
        # Actually set the font
        font = QFont(sets["Font_family"], sets["Font_size"])
        font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font)
        self.term_edit.setFont(font)

        ## Colors
        # Color Pallete
        self.setStyleSheet(f"""
            QWidget {{
                background-color : {load_color('Background', defaults, sets, fails)};
                color : {load_color('Foreground', defaults, sets, fails)};
            }}
            
            QScrollBar:vertical{{
                background : {load_color('Background', defaults, sets, fails)};
                width : 12px;
                margin : 0px 0px 0px 0px;
            }}

            QTermEdit{{
                background-color : {load_color('Background', defaults, sets, fails)};
                border : 1px solid {load_color('Cursor', defaults, sets, fails)};
                color : {load_color('Foreground', defaults, sets, fails)};
            }}

            QFrame{{
                background-color : {load_color('Frame_color', defaults, sets, fails)};
                border : 1px solid {load_color('Foreground', defaults, sets, fails)};
                border-radius : 4px;
            }}""")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.term_edit)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.term_edit.setFont(font)

def main(vfs):
    app = QApplication(sys.argv)
    window = TerminalWindow(vfs)
    window.show()
    sys.exit(app.exec())
