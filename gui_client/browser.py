from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLayout, QLineEdit, QPushButton, QTextEdit, QSplitter, \
    QVBoxLayout, QTabWidget, QAction, QGridLayout, QTextBrowser
from PyQt5.QtGui import QIcon, QTextCursor, QTextCharFormat, QBrush, QColor
from PyQt5.QtCore import Qt, QUrl
import sys
import selectors
import traceback
import socket
from urllib import parse
from message import ClientMessage
from gui_client.ui.error_page import general_error

sel = selectors.DefaultSelector()


class BrowserWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.layout = QGridLayout(self)

        self.textbox = QLineEdit(self)
        self.textbox.setText('virgo://')
        self.textbox.resize(280, 40)
        self.textbox.returnPressed.connect(self.on_click_go)

        self.gobutton = QPushButton('Go', self)
        self.gobutton.clicked.connect(self.on_click_go)

        self.textcontent = QTextBrowser(self)
        self.textcontent.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.textcontent.setOpenLinks(False)
        self.textcontent.anchorClicked.connect(self.go_to)

        self.layout.addWidget(self.textbox, 0, 0)
        self.layout.addWidget(self.gobutton, 0, 1)
        self.layout.addWidget(self.textcontent, 1, 0)

        self.setLayout(self.layout)

    def go_to(self, url):
        self.parent.new_browser_window()
        self.parent.current_browser_window.open_link(parse.urlparse(url.toString()))

    def create_request(self, type, file, metadata):
        if type == "aquire":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(type=type, file=file, metadata=metadata),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(type + file, encoding="utf-8"),
            )

    def start_connection(self, host, port, request):
        addr = (host, port)
        print("starting connection to", addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = ClientMessage(sel, sock, addr, request)
        sel.register(sock, events, data=message)

    def on_click_go(self):
        self.open_link(parse.urlparse(self.textbox.text(), 'virgo://'))

    def find_all(self, text):
        self.textcontent.textCursor().beginEditBlock()
        doc = self.textcontent.document()
        cursor = QTextCursor(doc)
        text_format = QTextCharFormat()
        text_format.setBackground(QBrush(QColor("yellow")))
        while True:
            cursor = doc.find(text, cursor)
            if cursor.isNull():
                break
            # cursor.insertText('new') # use for replace all later..
            cursor.mergeCharFormat(text_format)
        self.textcontent.textCursor().endEditBlock()

    def open_link(self, url):
        self.textbox.setText(url.geturl())
        print(url)
        if url.netloc == 'about':
            about_page = """
                <style>
                    h1 {
                        text-align: center;
                    }
                </style>
                <h1>About</h1>
                <p>This is an experimental client to interact with the virgo protocol.</p>
                <ul>
                    <li><p>Client version: Unknown</p></li>
                    <li><p>Supported virgo protocol version: Unknown</p></li>
                    <li><a href="http://github.com/Mozzo1000/virgo">Virgo source code and specification</a></li>
                </ul>
                <h2>Test pages</h2>
                <ul>
                    <li><a href="virgo://localhost">localhost</a></li>
                    <li><a href="virgo://localhost/index.html">localhost/index.html</a></li>
                    <li><a href="virgo://localhost/alice29.txt">alice29.txt</a></li>
                    <li><a href="virgo://localhost/lcet10.txt">lcet10.txt</a></li>
                    <li><a href="virgo://localhost/plrabn12.txt">plrabn12.txt</a></li>
                    <li><a href="virgo://localhost/text.txt">text test</a></li>
                    <li><a href="virgo://localhost/text2.txt">text test 2</a></li>
                </ul>                
            """
            self.parent.tab_widget.setTabText(self.parent.tab_widget.currentIndex(), 'About')
            self.textcontent.setText(about_page)

        elif url.scheme == 'virgo':
            host = url.netloc
            path = url.path
            port = 1784

            request = self.create_request('aquire', path, 'None')
            try:
                self.start_connection(host, port, request)
            except socket.gaierror:
                self.textcontent.setHtml(general_error)
            while True:
                events = sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                        self.textcontent.setText(message.accepted_message)
                        self.parent.tab_widget.setTabText(self.parent.tab_widget.currentIndex(), url.netloc + url.path)
                    except ConnectionRefusedError:
                        self.textcontent.setHtml(general_error)
                    except Exception:
                        print(
                            "main: error: exception for",
                            f"{message.addr}:\n{traceback.format_exc()}",
                        )
                        message.close()
                # Check for a socket being monitored to continue.
                if not sel.get_map():
                    break







