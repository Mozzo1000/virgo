import selectors
import traceback
import socket
import json
from urllib import parse
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, \
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QUrl
from message import ClientMessage

sel = selectors.DefaultSelector()


class Index(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Index')
        self.host = parent.current_browser_window.get_active_host()[0]
        self.port = parent.current_browser_window.get_active_host()[1]

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        table = QTableWidget(self)
        table.setColumnCount(2)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        table.setHorizontalHeaderLabels(['Link', 'Last mod'])
        table.horizontalHeader().setStretchLastSection(True)
        table.doubleClicked.connect(self.clicked_item)

        request = self.create_request('index', '', '')
        try:
            self.start_connection(self.host, self.port, request)
        except socket.gaierror:
            print('error')
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                    if message.response:
                        json_obj = json.loads(message.response.get('body'))
                        self.domain = json_obj['domain']
                        self.setWindowTitle('Index - ' + self.domain)
                        table.setRowCount(len(json_obj['pages']))
                        count = 0
                        for item in json_obj['pages']:
                            table.setItem(count, 0, QTableWidgetItem(item['page']))
                            table.setItem(count, 1, QTableWidgetItem(item['lastmod']))
                            count += 1

                except ConnectionRefusedError:
                    print('error')
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break

        layout.addWidget(table)
        central_widget.setLayout(layout)

    def clicked_item(self, index):
        if index.column() == 0:
            link = QUrl('virgo://' + self.domain + index.data())
            self.parent.current_browser_window.go_to(link)

    def create_request(self, type, file, metadata):
        if type == "aquire":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(type=type, file=file, metadata=metadata),
            )
        if type == "index":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(type=type)
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