from PySide6.QtCore import Qt, QProcess, QEvent
from PySide6.QtGui import QFontDatabase, QFont, QTextCursor, QTextOption
from PySide6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from utils import module_registry, module_dir_registry
from utils.window.loads import defaults, load_sets
from utils.window.CursorManager import Cursor_Manager
from utils.window.EventHandler import eventHandler
from utils.window.prompt import Prompt

sets = load_sets(defaults)

class QTermEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cursor_manager = Cursor_Manager(self)
        self.event_handler = eventHandler(self)
        self.prompt = Prompt(self)
              
        ## Import vfs
        self.vfs = parent.vfs

        ## Font setting
        font = QFont(parent.font())
        font.setStyleStrategy(QFont.PreferAntialias)
        font.setStyleHint(QFont.Monospace)
        text_option = self.document().defaultTextOption()
        text_option.setFlags(text_option.flags() | QTextOption.IncludeTrailingSpaces)
        self.document().setDefaultTextOption(text_option)

        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setReadOnly(False)
        self.input_buffer = ""
        self.history = []
        self.history_index = -1
        self.setFont(font)
        if parent.startup_messages:
            self.insertPlainText(str(parent.startup_messages)+"\n")
       
        prompt = self.prompt.load(sets["Background"], "normal")
        self.insertHtml(prompt)
        self.input_start_pos = self.textCursor().position()

        self.installEventFilter(self.event_handler)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.cursor_manager.enforce_input_zone()