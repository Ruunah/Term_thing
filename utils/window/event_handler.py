from PySide6.QtCore import QObject

class eventHandler(QObject):
    def __init__(self, term):
        .super().__init__(term)
        if obj == self and event.type() == QEvent.KeyPress:
            key = event.key()
            text = event.text()

            match key:
                case Qt.Key_Return | Qt.Key_Enter:
                    cursor = self.textCursor
                    cursor.movePosition(QTextCursor.EndOfLine)
                    self.setTextCursor(cursor)
                    cmd = (self.input_buffer.replace("cd..", "cd  ..", 1).split()) #I couldnt figure out how to make it properly so suffer while I dont implement aliases
                    if len(cmd) > 1:
                       command = cmd[0]
                       args = cmd[1:]
                       if len(args)<=1:
                           args=str(args[0])
                       self.run_command(command_registry, command, args)
                    
                    else:
                        command = self.input_buffer.strip()
                        self.run_command(command_registry, command)

                    prompt = self.prompt("normal")
                    self.insertHtml(prompt)
                    self.history.append(self.input_buffer)
                    self.input_buffer = ""
                    self.history_index = len(self.history)
                    return True

                case Qt.Key_Backspace:
                    if len(self.input_buffer) > 0:
                        self.input_buffer = self.input_buffer[:-1]
                        cursor = self.textCursor()
                        cursor.deletePreviousChar()
                    return True

                case Qt.Key_Up:
                    # History up
                    if self.history and self.history_index > 0:
                        self.history_index -= 1
                        self.replace_current_line(self.history[self.history_index])
                    return True

                case Qt.Key_Down:
                    # History down
                    if self.history and self.history_index < len(self.history) - 1:
                        self.history_index += 1
                        self.replace_current_line(self.history[self.history_index])
                    else:
                        self.history_index = len(self.history)
                        self.replace_current_line("")
                    return True

                case Qt.Key_Left:
                    self.cursor_manager
                    return True

                case _:
                    if text.isprintable():
                        self.input_buffer += text
                        self.insertPlainText(text)
                        return True

        return super().eventFilter(obj, event)

    def replace_current_line(self, text):
        cursor = self.textCursor()
        for _ in range(len(self.input_buffer)):
            cursor.deletePreviousChar()
        self.input_buffer = text
        self.insertPlainText(text) 

    def run_command(self, command_registry, command="", args=""):
        # Transient Prompt
        cursor = self.textCursor()
        for _ in range(len(self.input_buffer)+3):
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)

        cursor.movePosition(QTextCursor.Up, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        self.insertHtml(self.prompt(sets["Background"], "transient"))
        self.insertHtml(f"""<span style='color:#ffffff; background-color:sets{["Background"]}'>{self.input_buffer}</span>""")
        
        # Command execution
        if command:
            if command in command_registry:
                command_registry[command](self, args)

            elif command.strip():
                self.insertPlainText("\nCommand Not found\n")

        else:
            self.insertPlainText("\n")

