import sys
from urllib import parse
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QAction, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QApplication, qApp

from ui.find import Find
from browser import BrowserWindow
from ui.index import Index
from toolbar import Toolbar


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Virgo Browser')

        self.window = QWidget()
        self.window.resize(800, 700)

        self.browser_windows = []

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabShape(QTabWidget.Rounded)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.currentChanged.connect(self.change_browser_window)
        self.tab_widget.tabCloseRequested.connect(self.remove_browser_window)

        self.toolbar = Toolbar(self)

        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.toolbar)

        self.new_browser_window()
        # Open about page on launch
        self.current_browser_window.open_link(parse.urlparse('virgo://about'))

        exit_action = QAction(QIcon('exit.png'), ' &Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        new_tab_action = QAction('&New tab', self)
        new_tab_action.setShortcut('Ctrl+N')
        new_tab_action.triggered.connect(self.new_browser_window)

        close_current_tab_action = QAction('&Close current tab', self)
        close_current_tab_action.setShortcut('Ctrl+W')
        close_current_tab_action.triggered.connect(self.close_tab)

        get_index_action = QAction('&Retrieve index', self)
        get_index_action.triggered.connect(self.get_index_window)

        find_all_action = QAction('Find all', self)
        find_all_action.setShortcut('Ctrl+F')
        find_all_action.triggered.connect(self.find_all_window)

        bookmark_manager_action = QAction('&Bookmark manager', self)
        bookmark_manager_action.setStatusTip('Bookmark manager')

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(new_tab_action)
        file_menu.addAction(close_current_tab_action)
        file_menu.addAction(get_index_action)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('&Edit')
        edit_menu.addAction(find_all_action)

        bookmark_menu = menubar.addMenu("&Bookmarks")
        bookmark_menu.addAction(bookmark_manager_action)

        self.layout.addWidget(menubar)

        self.window.setLayout(self.layout)
        self.window.show()

    def get_index_window(self):
        index = Index(self)
        index.show()

    def find_all_window(self):
        find_all = Find(self.current_browser_window)
        find_all.show()

    def close_tab(self):
        self.remove_browser_window(self.tab_widget.currentIndex())

    def create_browser_window(self):
        browser_window = BrowserWindow(self)
        return browser_window

    def remove_browser_window(self, index):
        if index is False:
            index = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(index)
        if index < len(self.browser_windows):
            del self.browser_windows[index]

        if self.tab_widget.count() < 1:
            self.new_browser_window('')
            self.current_browser_window.open_link(parse.urlparse('virgo://about'))

    def change_browser_window(self, index):
        if index < len(self.browser_windows):
            self.current_browser_window = self.browser_windows[index]
            if self.current_browser_window.url:
                self.toolbar.set_addressbar_text(self.current_browser_window.url.geturl())

    def new_browser_window(self, title="New tab"):
        # For some reason, when creating a new tab it returns False..
        # We fix this by setting the name if title does not exists / returns false or
        # if the title already is set to "New tab"
        if not title or title == "New tab":
            title = "New tab"
        browser_window = self.create_browser_window()
        self.browser_windows.append(browser_window)
        self.tab_widget.addTab(browser_window, title)
        self.toolbar.set_addressbar_text('virgo://')
        self.tab_widget.setCurrentWidget(browser_window)


if __name__ == '__main__':
    print("Starting virgo browser..")
    app = QApplication(sys.argv)
    browser = Browser()
    sys.exit(app.exec_())
