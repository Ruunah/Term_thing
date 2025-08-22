from PySide6.QtWidgets import QApplication, QListWidget, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
import sys

class SuggestionPopup(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | 
                            Qt.Tool |  # So it behaves like a popup
                            Qt.FramelessWindowHint)
        self.resize(200, 150)

    def show_suggestions(self, suggestions, position):
        self.clear()
        self.addItems(suggestions)
        self.move(position)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_win = QWidget()
    main_win.setWindowTitle("Main Window")
    main_win.resize(300, 200)

    layout = QVBoxLayout(main_win)
    button = QPushButton("Show Suggestions")
    layout.addWidget(button)

    popup = SuggestionPopup(main_win)

    def on_click():
        suggestions = ["command1", "command2", "command3", "another_command"]
        # Show popup below the button
        pos = button.mapToGlobal(button.rect().bottomLeft())
        popup.show_suggestions(suggestions, pos)

    button.clicked.connect(on_click)

    main_win.show()
    sys.exit(app.exec())
