import re
import os
import sys
import tomllib
from PySide6.QtCore import Qt
from utils.window.QTermEdit import QTermEdit
from PySide6.QtGui import QFontDatabase, QFont, QColor, QPalette, QPainter
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsOpacityEffect
from utils.window.loads import defaults, load_sets, load_font, load_color

def hex_to_rgb(color: str, opacity=0.85) -> QColor:
    color = color.strip().lstrip("#")

    try:

        opacity=float(opacity)

        if len(color) != 6:
            raise(ValueError)

        if not(0.0 <= opacity <= 1.0):
            raise(ValueError)

        else:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)

        return QColor(r, g, b, (opacity*255))

    except:
        return QColor(1, 22, 39, (0.85*255))



class TerminalWindow(QWidget):
    def __init__(self, vfs):
        super().__init__()
        self.vfs = vfs
        self.startup_messages = []
        self.initUI()

    def initUI(self):
        self.term_edit = QTermEdit(self)
        result = load_sets(defaults)
        if isinstance(result, tuple):
            sets, msg = result
            fails = msg[1:]
            self.startup_messages.append(msg[0])

        else:
            fails=[]
            sets = result
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)


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


        self.rgba = hex_to_rgb(sets["Background"], sets["Opacity"])



        ## Colors
        # Color Pallete
        self.setStyleSheet(f"""
            QScrollBar:vertical{{
                background : {load_color('Background', defaults, sets, fails)};
                width : 12px;
                margin : 0px 0px 0px 0px;
            }}

            QTermEdit{{
                background-color : transparent;
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


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.rgba)

def main(vfs):
    app = QApplication(sys.argv)
    window = TerminalWindow(vfs)
    window.show()
    sys.exit(app.exec())