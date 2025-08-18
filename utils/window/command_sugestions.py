from PySide6.QtGui import QColor, QPainter, QFontMetrics
from PySide6.QtCore import QPoint
from utils.window.loads import defaults, load_sets, hex_to_rgb
from commands import command_registry

self = load_sets(defaults)

class GhostTextMixin(parent=""):
    def __init__(self):
        self._ghost_text = ""
        self._ghost_color = QColor(hex_to_rgb(self["Foreground"], "0.5"))
        self.parent = parent

    def check(self):
        if self.parent.command 