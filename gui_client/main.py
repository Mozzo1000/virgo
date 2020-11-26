import sys
from urllib import parse
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLayout, QSplitter, QTabWidget, QAction, QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.Qt import QApplication, qApp

from ui.find import Find
from browser import BrowserWindow
from ui.index import Index


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Virgo Browser')
        self.central_widget = QWidget(self)

        self.horizontal_layout = QHBoxLayout(self.central_widget)
        self.horizontal_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.splitter = QSplitter(self.central_widget)

        self.browser_windows = []

        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setTabShape(QTabWidget.Rounded)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.currentChanged.connect(self.change_browser_window)
        self.tab_widget.tabCloseRequested.connect(self.remove_browser_window)
        self.new_browser_window()

        # Open about page on launch
        self.current_browser_window.open_link(parse.urlparse('virgo://about'))

        self.splitter.addWidget(self.tab_widget)
        self.horizontal_layout.addWidget(self.splitter)

        self.setCentralWidget(self.central_widget)

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

        self.show()

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

    def change_browser_window(self, index):
        if index < len(self.browser_windows):
            self.current_browser_window = self.browser_windows[index]

    def new_browser_window(self, title="New tab"):
        # For some reason, when creating a new tab it returns False..
        # We fix this by setting the name if title does not exists / returns false or
        # if the title already is set to "New tab"
        if not title or title == "New tab":
            title = "New tab"
        browser_window = self.create_browser_window()
        self.browser_windows.append(browser_window)
        self.tab_widget.addTab(browser_window, title)
        self.tab_widget.setCurrentWidget(browser_window)

if __name__ == '__main__':
    print("Starting virgo browser..")
    app = QApplication(sys.argv)
    browser = Browser()
    sys.exit(app.exec_())
