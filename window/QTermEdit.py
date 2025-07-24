from PySide6.QtCore import Qt, QProcess, QEvent
from PySide6.QtGui import QFontDatabase, QFont, QTextCursor, QTextOption
from PySide6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout


class QTermEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont(parent.font())
        font.setStyleStrategy(QFont.PreferAntialias)
        font.setStyleHint(QFont.Monospace)

        text_option = self.document().defaultTextOption()
        text_option.setFlags(text_option.flags() | QTextOption.IncludeTrailingSpaces)
        self.document().setDefaultTextOption(text_option)

        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setReadOnly(False)
        self.prompt = "--> "
        self.insertPlainText(self.prompt)
        self.input_buffer = ""
        self.history = []
        self.history_index = -1
        self.setFont(font)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self and event.type() == QEvent.KeyPress:
            key = event.key()
            text = event.text()

            if key in (Qt.Key_Return, Qt.Key_Enter):
                command = self.input_buffer.strip()
                self.insertPlainText("")  # Move to next line
                self.run_command(command)
                self.insertPlainText(self.prompt)
                self.input_buffer = ""
                self.history.append(command)
                self.history_index = len(self.history)
                return True

            elif key == Qt.Key_Backspace:
                if len(self.input_buffer) > 0:
                    self.input_buffer = self.input_buffer[:-1]
                    cursor = self.textCursor()
                    cursor.deletePreviousChar()
                return True

            elif key == Qt.Key_Up:
                # History up
                if self.history and self.history_index > 0:
                    self.history_index -= 1
                    self.replace_current_line(self.history[self.history_index])
                return True

            elif key == Qt.Key_Down:
                # History down
                if self.history and self.history_index < len(self.history) - 1:
                    self.history_index += 1
                    self.replace_current_line(self.history[self.history_index])
                else:
                    self.history_index = len(self.history)
                    self.replace_current_line("")
                return True

            elif text.isprintable():
                self.input_buffer += text
                self.insertPlainText(text)
                return True

        return super().eventFilter(obj, event)

    def replace_current_line(self, text):
        # Remove current input buffer text from widget and replace with `text`
        cursor = self.textCursor()
        for _ in range(len(self.input_buffer)):
            cursor.deletePreviousChar()
        self.input_buffer = text
        self.insertPlainText(text)

    def run_command(self, command):
        # Define your custom commands here
        if command == "hello":
            self.insertPlainText("\n"+"Hello! This is your custom command terminal."+"\n")
        elif command == "help":
            self.insertPlainText("\n"+"Available commands: hello, help, clear"+"\n")
        elif command == "clear":
            self.clear()
        elif command == "":
            self.insertPlainText("\n")
            pass  # Ignore empty command
        else:
            self.insertPlainText("\n"+f"Unknown command: {command}"+"\n")

