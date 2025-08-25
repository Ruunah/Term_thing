from PySide6.QtCore import Qt, QProcess, QEvent, QPoint
from PySide6.QtGui import QFontDatabase, QFont, QTextCursor, QTextOption
from PySide6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from utils import module_registry, module_dir_registry
from utils.window.loads import defaults, load_sets
from utils.window.CursorManager import Cursor_Manager
from utils.window.EventHandler import eventHandler
from utils.window.prompt import load as Prompt
from utils.window.command_suggestions import SuggestionPopup

sets = load_sets(defaults)

class QTermEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cursor_manager = Cursor_Manager(self)
        self.suggestion_popup = SuggestionPopup(self)
        self.event_handler = eventHandler(self)
        self.prompt = Prompt
              
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
       
        prompt = self.prompt(self, sets["Background"], "normal")
        self.insertHtml(prompt)
        self.input_start_pos = self.textCursor().position()

        self.installEventFilter(self.event_handler)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.cursor_manager.enforce_input_zone()



    def show_suggestions(self):
        cursor_rect = self.cursorRect()
        global_pos = self.mapToGlobal(cursor_rect.bottomRight())
        self.suggestion_popup.update_suggestions(self.input_buffer, global_pos)

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Up, Qt.Key_Down) and self.suggestion_popup.isVisible():
            self.suggestion_popup.setFocus()
            self.suggestion_popup.keyPressEvent(event)
            return

        elif key in (Qt.Key_Enter, Qt.Key_Return) and self.suggestion_popup.isVisible():
            selected = self.suggestion_popup.get_selected_command()
            if selected:
                self.cursor_manager.replace_current_line(selected)
                self.input_buffer = selected
                self.suggestion_popup.hide()
                return
        else:
            super().keyPressEvent(event)
            self.show_suggestions()
