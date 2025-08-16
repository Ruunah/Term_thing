from PySide6.QtCore import Qt, QProcess, QEvent
from PySide6.QtGui import QFontDatabase, QFont, QTextCursor, QTextOption
from PySide6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from commands import command_registry
from utils import module_registry, module_dir_registry
from utils.window.loads import defaults, load_sets

sets = load_sets(defaults)

class QTermEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
              
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
       
        prompt = self.prompt("normal")
        self.insertHtml(prompt)


        self.input_start_pos = self.textCursor().position()

        cursor = self.textCursor()

        if cursor.position() < self.input_start_pos:
            cursor.setPosition(self.document().characterCount() -1)
            self.setTextCursor(cursor)
            return True


        self.installEventFilter(self)
    

    

    def eventFilter(self, obj, event):
        if obj == self and event.type() == QEvent.KeyPress:
            key = event.key()
            text = event.text()

            if key in (Qt.Key_Return, Qt.Key_Enter):
                if len(self.input_buffer.replace("cd..", "cd ..", 1).split()) > 1:
                   cmd = self.input_buffer.replace("cd..", "cd  ..", 1).split()
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
        cursor = self.textCursor()
        for _ in range(len(self.input_buffer)):
            cursor.deletePreviousChar()
        self.input_buffer = text
        self.insertPlainText(text) 

    def run_command(self, command_registry, command="", args=""):
        cursor = self.textCursor()
        for _ in range(len(self.input_buffer)+3):
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)

        cursor.movePosition(QTextCursor.Up, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        self.insertHtml(self.prompt("transient"))
        bg_color = sets["Background"]
        self.insertHtml(f"<span style='color:#ffffff; background-color:{bg_color}'>{self.input_buffer}</span>")

        if command:
            if command in command_registry:
                command_registry[command](self, args)

            elif command.strip():
                self.insertPlainText("\nCommand Not found\n")

        else:
            self.insertPlainText("\n")

    
  
    def prompt(self, style=""):
        bg_color = sets["Background"]
        try:
            match style:
                case "transient":
                    if self.vfs.cwd == self.vfs.root:
                        cwd = "<b>root<b>"

                    elif self.vfs.cwd == self.vfs.home:
                        cwd = " "

                    else:
                        cwd = str(self.vfs.cwd.relative_to(self.vfs.root)).replace("\\", "/").split("/")[-1]
                    
                    prompt=f"""<span style='color:#61AFEF; background-color:{bg_color}'></span><span style='color:#011627; background-color:#61AFEF'>{cwd}</span><span style='color:#61AFEF; background-color:{bg_color}'></span>"""

                    return prompt

                case "normal":
                    if self.vfs.cwd == self.vfs.root:
                        cwd = "<b>root <b>"

                    elif self.vfs.cwd == self.vfs.home:
                        cwd = " "

                    elif self.vfs.cwd.is_relative_to(self.vfs.home):
                        cwd = f" ❯<b>{str(self.vfs.cwd.relative_to(self.vfs.home))}<b>"

                    else:
                        cwd = self.vfs.cwd.relative_to(self.vfs.root)
                    
                    cwd = "❯".join(str(cwd).split("/"))+"❯ "
                    
                    prompt=f"""<span style='color:#ffffff; background-color:{bg_color}'>╭─</span><span style='color:#61AFEF; background-color:{bg_color}'></span><span style='color:#011627; background-color:#61AFEF'> </span><span style='color:#61AFEF; background-color:#ffafd2'></span><span style='color:#011627; background-color:#ffafd2'> {cwd}</span><span style='color:#ffafd2; background-color:{bg_color}'><br></span><span style='color:#ffffff; background-color:{bg_color}'>╰─</span>"""

                    return prompt

                case _:
                    raise(ValueError)

        except(ValueError):
            print("style can only be normal or transient")



    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.textCursor().position() < self.input_start_pos:
            self.movePosition(QTextCursor.End)
