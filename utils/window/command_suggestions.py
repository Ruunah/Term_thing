from PySide6.QtGui import QColor, QPainter, QFontMetrics
from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import QPoint
from utils.window.loads import defaults, load_sets, hex_to_rgb
from commands import command_registry

sets = load_sets(defaults)

class PopupWindow(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.WindowStaysOnTopHint |
        Qt.WindowType.Tool
        )

        ## Font setting
        font = QFont(parent.font())
        font.setStyleStrategy(QFont.PreferAntialias)
        font.setStyleHint(QFont.Monospace)
        text_option = self.document().defaultTextOption()
        text_option.setFlags(text_option.flags() | QTextOption.IncludeTrailingSpaces)
        self.document().setDefaultTextOption(text_option)

        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setReadOnly(True)

        def update(self):
            list_widget.clear()
            self.suggestions.check_()
            for key in self._ghost_text.list:
                list_widget.addItems(key)

class GhostTextMixin():
    def __init__(self, parent=None):
        self._ghost_text.text = ""
        self._ghost_text.list = []
        self._ghost_text.color = QColor(hex_to_rgb(sets["Foreground"], "0.5"))
        self.parent = parent

    def check_(self):
        for key in command_registry:
            if self.parent.input_buffer in key:
                self._ghost_text.list.append(str(key).strip())
    
    def update_(self):
        self.check_()
        if self._ghost_text.list:
            if len(self._ghost_text.list) != 0:
                if len(self._ghost_text.list) <= 1:
                    self._ghost_text.text = str(self._ghost_text.list[0])[-len(self.parent.input_buffer)]

                else:
                    self.parent.sugestions.visual = PopupWindow(self.parent)
