from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt


class Find(QMainWindow):
    def __init__(self, text_window):
        super().__init__(text_window)
        self.setWindowTitle('Find')
        self.text_window = text_window

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.search_box = QLineEdit(self)
        self.search_box.returnPressed.connect(self.find_all)

        self.find_all_button = QPushButton("Find all", self)
        self.find_all_button.clicked.connect(self.find_all)


        layout.addWidget(self.search_box)
        layout.addWidget(self.find_all_button)

        central_widget.setLayout(layout)

    def find_all(self):
        self.text_window.find_all(self.search_box.text())
        self.close()

