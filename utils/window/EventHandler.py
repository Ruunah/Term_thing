from PySide6.QtGui import QTextCursor
from PySide6.QtCore import QObject, Qt, QEvent
from commands import command_registry
from utils.window.loads import load_sets, defaults
from utils.window.CursorManager import Cursor_Manager

sets = load_sets(defaults)

class eventHandler(QObject):
    def __init__(self, term):
        super().__init__(term)
        self.term = term
        self.cursor_manager = Cursor_Manager(self.term)

    def eventFilter(self, obj, event):
        if obj == self.term and event.type() == QEvent.KeyPress:
            key = event.key()
            text = event.text()

            match key:
                case Qt.Key_Return | Qt.Key_Enter:
                    cursor = self.term.textCursor()
                    cursor.movePosition(QTextCursor.EndOfLine)
                    self.term.setTextCursor(cursor)
                    cmd = (self.term.input_buffer.replace("cd..", "cd  ..", 1).split()) #I couldnt figure out how to make it properly so suffer while I dont implement aliases
                    if len(cmd) > 1:
                        command = cmd[0]
                        args = cmd[1:]
                        if len(args)<=1:
                            args=str(args[0])
                        self.run_command(command_registry, command, args)

                    else:
                        command = self.term.input_buffer.strip()
                        self.run_command(command_registry, command)

                    prompt = self.term.prompt(self.term, sets["Background"], "normal")
                    self.term.insertHtml(prompt)
                    self.term.history.append(self.term.input_buffer)
                    self.term.input_buffer = ""
                    self.term.history_index = len(self.term.history)
                    return True

                case Qt.Key_Backspace:
                    self.cursor_manager.delete_previous()
                    return True

                case Qt.Key_Up:
                    # History up
                    if self.term.history and self.term.history_index > 0:
                        self.term.history_index -= 1
                        self.cursor_manager.replace_current_line(self.term.history[self.term.history_index])
                    return True

                case Qt.Key_Down:
                    # History down
                    if self.term.history and self.term.history_index < len(self.term.history) - 1:
                        self.term.history_index += 1
                        self.cursor_manager.replace_current_line(self.term.history[self.term.history_index])
                    else:
                        self.term.history_index = len(self.term.history)
                        self.cursor_manager.replace_current_line("")
                    return True

                case Qt.Key_Left:
                    self.cursor_manager.safe_left()
                    return True

                case _:
                    if text.isprintable():
                        self.cursor_manager.insert_text(text)
                        return True

        return super().eventFilter(obj, event)

    def run_command(self, command_registry, command="", args=""):
        # Transient Prompt
        cursor = self.term.textCursor()
        for _ in range(len(self.term.input_buffer)+3):
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)

        cursor.movePosition(QTextCursor.Up, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        self.term.insertHtml(self.term.prompt(self.term, sets["Background"], "transient"))
        if self.term.input_buffer:
            self.term.insertHtml(f"""<span style='color:#ffffff; background-color:{sets["Background"]}'>{self.term.input_buffer}</span>""")
        
        # Command execution
        if command:
            if command in command_registry:
                command_registry[command](self.term, args)

            elif command.strip():
                self.term.insertPlainText("\nCommand Not found\n")

        else:
            self.term.insertPlainText("\n")
