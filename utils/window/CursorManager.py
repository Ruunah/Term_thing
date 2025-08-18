class Cursor_Manager:
    def __init__(self, term):
        self.term = term

    def move_to_end(self):
        cursor = self.term.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.term.setTextCursor(cursor)

    def safe_left(self):
        cursor = self.term.textCursor()
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
        self.term.setTextCursor(cursor)
        self.enforce_input_zone()

    def insert_text(self, text):
        self.term.input_buffer += text
        self.term.insertPlainText(text)
        self.term.move_to_end()

    def delete_previous(self):
        if self.term.input_buffer:
            self.term.input_buffer = self.term.input_buffer[:-1]
            cursor = self.term.textCursor()
            cursor.deletePreviousChar()
        
    def replace_current_line(self, text):
        cursor = self.term.textCursor()
        for _ in range(len(self.input_buffer)):
            self.term.delete_previous
        self.term.input_buffer = text
        self.term.insertPlainText(text) 
        
    def enforce_input_zone(self):
        cursor = self.term.textCursor
        if cursor.position() < self.input_start_pos:
            cursor.movePosition(self.input_start_pos)
            self.term.setTextCursor(cursor)