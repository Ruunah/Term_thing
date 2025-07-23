from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QFontDatabase, QFont, QTextCursor
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QWidget, QVBoxLayout


class CustomCommandTerminal(QPlainTextEdit):
    def __init__(self, font_family="JetBrains Mono", font_size=14, parent=None):
        super().__init__(parent)

        font = QFont(font_family, font_size)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font)

        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setReadOnly(False)

        self.prompt = ">>> "
        self.appendPlainText(self.prompt)
        self.input_buffer = ""
        self.history = []
        self.history_index = -1

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self and event.type() == event.KeyPress:
            key = event.key()
            text = event.text()

            if key in (Qt.Key_Return, Qt.Key_Enter):
                command = self.input_buffer.strip()
                self.appendPlainText("")  # Move to next line
                self.run_command(command)
                self.appendPlainText(self.prompt)
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
            self.appendPlainText("Hello! This is your custom command terminal.")
        elif command == "help":
            self.appendPlainText("Available commands: hello, help, clear")
        elif command == "clear":
            self.clear()
        elif command == "":
            pass  # Ignore empty command
        else:
            self.appendPlainText(f"Unknown command: {command}")

