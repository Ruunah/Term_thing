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

        self.setCursorWidth(0)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setReadOnly(False)
        self.input_buffer = ""
        self.history = []
        self.history_index = -1
        self.setFont(font)
        if parent.startup_messages:
            self.insertPlainText(str(parent.startup_messages)+"\n")
       
        prompt = self.prompt()
        self.insertHtml(prompt)

        self.installEventFilter(self)
    

        

    def eventFilter(self, obj, event):
        if obj == self and event.type() == QEvent.KeyPress:
            key = event.key()
            text = event.text()
            prompt = self.prompt()

            if key in (Qt.Key_Return, Qt.Key_Enter):
                if len(self.input_buffer.split()) > 1:
                   cmd = self.input_buffer.split() 
                   command = cmd[0]
                   args = cmd[1:]
                   if len(args)<=1:
                       args=str(args)
                   self.run_command(command_registry, command, args)

                elif len(self.input_buffer.split())> 0:
                    command = self.input_buffer.strip()
                    self.run_command(command_registry, command)

                else:
                    self.insertPlainText("\n")

                self.insertPlainText("")  # Move to next line
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
        # Remove current input buffer text from widget and replace with `text`
        cursor = self.textCursor()
        for _ in range(len(self.input_buffer)):
            cursor.deletePreviousChar()
        self.input_buffer = text
        self.insertPlainText(text)

    def run_command(self, command_registry, command, args=""):
        if command in command_registry:
            command_registry[command](self, args)

        elif command.strip():
            self.insertPlainText("\nCommand {command} Not found\n")
    
  
    def prompt(self):
        bg_color = sets["Background"]
        if self.vfs.cwd == self.vfs.root:
            cwd = "root"

        elif self.vfs.cwd == self.vfs.home:
            cwd = ""

        elif self.vfs.cwd.is_related_to(self.vfs.home):
            cwd = f" {str(self.vfs.cwd.relative_to(self.vfs.home))}"

        else:
            cwd = self.vfs.cwd.relative_to(self.vfs.root)
        
        cwd = "❯".join(str(cwd).split("/"))
        
        prompt=f"""<span style='color:#ffffff; background-color:{bg_color}'>╭─</span><span style='color:#61AFEF; background-color:{bg_color}'></span><span style='color:#011627; background-color:#61AFEF'>  </span><span style='color:#61AFEF; background-color:#ffafd2'></span><span style='color:#011627; background-color:#ffafd2'>{cwd}</span><span style='color:#011627; background-color:{bg_color}'> </span><br>"""

        return prompt
