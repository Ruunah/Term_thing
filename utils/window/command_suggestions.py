from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QColor, QFont, QPalette
from commands import command_registry
from utils.window.loads import load_sets, defaults, hex_to_rgb

sets = load_sets(defaults)

class SuggestionPopup(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.NoDropShadowWindowHint
        )

        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(sets["Black"]))
        palette.setColor(QPalette.Text, QColor(sets["Foreground"]))
        self.setPalette(palette)

        font = QFont(parent.font())
        font.setPointSize(sets["Font_size"])
        font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font)
 
        self.setFocusPolicy(Qt.NoFocus)
        self.setMouseTracking(True)
        self.setSelectionMode(QListWidget.SingleSelection)

    def update_suggestions(self, term_input: str, position: QPoint):
        self.clear()

        if not term_input.strip():
            self.hide()
            return

        matches = [cmd for cmd in command_registry if term_input in cmd]

        if not matches:
            self.hide()
            return

        for cmd in matches:
            self.addItem(QListWidgetItem(cmd))

        self.setCurrentRow(0)
        self.move(position)
        self.setMinimumWidth(200)
        self.setMaximumHeight(150)
        self.show()

    def get_selected_command(self):
        item = self.currentItem()
        return item.text() if item else None

