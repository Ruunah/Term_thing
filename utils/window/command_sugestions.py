from PySide6.QtGui import QColor, QPainter, QFontMetrics
from PySide6.QtCore import QPoint
from utils.window.loads import defaults, load_sets, hex_to_rgb

self = load_sets(defaults)

class GhostTextMixin:
    def __init__(self):
        self._ghost_text = ""
        self._ghost_color = QColor(hex_to_rgb(self["Foreground"]))
