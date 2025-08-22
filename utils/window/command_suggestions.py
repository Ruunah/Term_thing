from PySide6.QtGui import QColor, QPainter, QFontMetrics
from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import QPoint
from utils.window.loads import defaults, load_sets, hex_to_rgb
from commands import command_registry

sets = load_sets(defaults)

class Suggestion():
    def __init__(self):
        super().__init__()
        self.update()

    def window(self, term):
        list_widget = QListWidget()
        self.update()

        list_widget.clear()
        self.suggestions.check_()
        for key in self.term.suggestions.text:
            list_widget.addItem(key)

    def update(self, term):
        self.term = term
        if self.term.input_buffer:
            self.match = []
            for key in command_registry:
                if self.term.input_buffer in key:
                    self.match.append(key.strip())
            if self.match:
                if len(self.match) <= 1:
                    self.term.suggestions.text = self.match[0]
                    self.term.suggestions.color = QColor(hex_to_rgb(sets["Foreground"], "0.5"))

                else:
                    self.term.SuggestionWindow
