from PySide6.QtWidgets import QWidget, QHBoxLayout, QTextBrowser
from PySide6.QtCore import QUrl, QSettings
from PySide6.QtGui import Qt

from utils import relPath
import webbrowser

class HelpWindow(QWidget):
    def __init__(self, parent, settings: QSettings):
        super().__init__(parent)
        # self.setWindowTitle("Manuale")
        # self.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint, True)
        # self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.settings = settings
        geometry = self.settings.value("helpwindow/geometry")
        if geometry==None:
            self.setGeometry(100, 100, 800, 600)
        else:
            self.restoreGeometry(geometry)
        self.setLayout(QHBoxLayout(self))

        self.index = QTextBrowser(self)
        self.index.setOpenLinks(False)
        self.view = QTextBrowser(self)
        self.view.setOpenLinks(False)
        self.view.setSearchPaths([relPath(p) for p in ["help", "help/img"]])
        self.layout().addWidget(self.index, stretch=1)
        self.layout().addWidget(self.view, stretch=3)
        self.index.anchorClicked.connect(self.linkClicked)
        self.view.anchorClicked.connect(self.linkClicked)

        with open(relPath(f"help/help.css"), "r", encoding="utf-8") as styleSheet:
            self.pageStyle = f"<style>{styleSheet.read()}</style>"
        with open(relPath(f"help/index.html"), "r", encoding="utf-8") as htmlPage:
            content = f"{self.pageStyle}{htmlPage.read()}"
            self.index.setHtml(content)
        self.loadPage("editor.html")
        pass

    def loadPage(self, fileName:str):
        split = fileName.split("#")
        with open(relPath(f"help/{split[0]}"), "r", encoding="utf-8") as htmlPage:
            content = f"{self.pageStyle}{htmlPage.read()}"
            self.view.setHtml(content)
            anchor = split[1] if len(split) > 1 else ""
            if (anchor != ""):
                self.view.scrollToAnchor(anchor)
        pass

    def linkClicked(self, url:QUrl):
        if url.url().find("http://") >= 0 or url.url().find("https://") >= 0 or url.url().find("mailto:") >= 0:
            webbrowser.open(url.url())
            return
        self.loadPage(url.url())
        pass

    def closeEvent(self, event):
        self.settings.setValue("helpwindow/geometry", self.saveGeometry())
        event.accept()