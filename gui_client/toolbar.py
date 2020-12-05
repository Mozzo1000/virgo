from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from urllib import parse


class Toolbar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.toolbar_layout = QHBoxLayout()
        self.addressbar = QLineEdit()
        self.addressbar.setText('virgo://')
        self.addressbar.returnPressed.connect(self.on_click_go)

        self.add_tab_button = QPushButton("+")
        self.add_tab_button.clicked.connect(self.on_click_add)

        self.go_button = QPushButton('Go')
        self.go_button.clicked.connect(self.on_click_go)

        self.toolbar_layout.addWidget(self.add_tab_button)
        self.setLayout(self.toolbar_layout)
        self.toolbar_layout.addWidget(self.addressbar)
        self.toolbar_layout.addWidget(self.go_button)

    def set_addressbar_text(self, text):
        self.addressbar.setText(text)

    def on_click_go(self):
        self.parent.current_browser_window.open_link(parse.urlparse(self.addressbar.text(), 'virgo://'))

    def on_click_add(self):
        self.parent.new_browser_window()
