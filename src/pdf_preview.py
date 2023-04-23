from PySide6.QtCore import Qt #, QSize
from PySide6.QtWidgets import QWidget, QStyle, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QToolBar, QLabel # QSpinBox, QSizePolicy, QMainWindow, QHBoxLayout
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QPainter, QPixmap # QImage
from utils import relPath

# Anteprima PDF

class PdfPreview(QWidget):
    zoomOptions = {
        0: ("Adatta alla larghezza", QPdfView.ZoomMode.FitToWidth, 1),
        1: ("Adatta alla pagina", QPdfView.ZoomMode.FitInView, 1),
        2: ("25%", QPdfView.ZoomMode.Custom, 0.25),
        3: ("50%", QPdfView.ZoomMode.Custom, 0.5),
        4: ("75%", QPdfView.ZoomMode.Custom, 0.75),
        5: ("90%", QPdfView.ZoomMode.Custom, 0.9),
        6: ("100%", QPdfView.ZoomMode.Custom, 1),
        7: ("125%", QPdfView.ZoomMode.Custom, 1.25),
        8: ("150%", QPdfView.ZoomMode.Custom, 1.5),
        9: ("200%", QPdfView.ZoomMode.Custom, 2),
    }
    currentZoomOption = 0
    currentPage = 1

    def __init__(self, parent=None):
        super().__init__(parent)

        #self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #self.resize(600,600)
        self.setLayout(QVBoxLayout())
        self.pdf_document = QPdfDocument(self) # QUrl()

        # Vista PDF
        
        self.pdf_view = QPdfView(self)
        self.pdf_view.resize(600, 400)
        self.pdf_view.setDocument(self.pdf_document)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)

        # Controlli zoom e pagina

        self.toolbar = QToolBar("Controlli pdf", self)
        #self.toolbar.setLayout(QHBoxLayout())
        #self.toolbar.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)
        #self.toolbar.setContentsMargins(0,0,0,0)
        #self.toolbar.layout().setContentsMargins(0,0,0,0)
        #self.toolbar.layout().setSpacing(0)

        self.zoom_selector = QComboBox(self.toolbar)
        self.zoom_selector.addItems([self.zoomOptions[i][0] for i in self.zoomOptions])
        self.zoom_selector.setCurrentText("Adatta alla larghezza")
        self.zoom_selector.currentIndexChanged.connect(self.setZoom)
        self.zoom_in_btn = QPushButton("\U0001f50D+")
        self.zoom_out_btn = QPushButton("\U0001f50D-")
        self.zoom_in_btn.clicked.connect(self.zoomIn)
        self.zoom_out_btn.clicked.connect(self.zoomOut)
        self.toolbar.addWidget(self.zoom_selector)
        self.toolbar.addWidget(self.zoom_out_btn)
        self.toolbar.addWidget(self.zoom_in_btn)
        self.toolbar.addSeparator()

        #self.toolbar.addSeparator()

        # TODO: azioni x controlli pagina
        self.prev_page_btn = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack), "", self.toolbar)
        self.next_page_btn = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward), "", self.toolbar)
        self.page_indicator = QLabel("1 / 1", self.toolbar)
        self.toolbar.addWidget(QLabel("Pagina "))
        self.toolbar.addWidget(self.prev_page_btn)
        self.toolbar.addWidget(self.page_indicator)
        self.toolbar.addWidget(self.next_page_btn)

        # Layout

        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.pdf_view)

        # Style
        self.setStyleSheet(
        """
        QComboBox { padding: 2px; }
        QPushButton, QLabel { border: none; margin: 2px; padding: 2px; padding-top: 3px; padding-bottom: 2px; border: 1px solid transparent; }
        QPushButton:hover { border: 1px solid #348cfa; background-color: #e4f3ff }
        QPushButton:pressed { padding: 1px -1px -1px 1px; background-color: #add8e6 }
        """
        )
    
    def loadPdf(self, pdf):
        self.pdf_document.load(pdf)
    
    def clearPdf(self):
        self.pdf_document.close()

    def toQImage(self):
        img = self.pdf_document.render(0, self.pdf_document.pagePointSize(0).toSize())
        img_with_white_bg = QPixmap(img.size())
        img_with_white_bg.fill("#ffffff")
        painter = QPainter()
        painter.begin(img_with_white_bg)
        painter.drawImage(0, 0, img)
        painter.end()
        return img_with_white_bg
    
    def setZoom(self, zoomSelection):
        self.currentZoomOption = zoomSelection
        zoom = self.zoomOptions[self.currentZoomOption]
        self.pdf_view.setZoomMode(zoom[1])
        self.pdf_view.setZoomFactor(zoom[2])
        pass

    def zoomIn(self):
        newZoom = 0
        if self.pdf_view.zoomMode() != QPdfView.ZoomMode.Custom:
            newZoom = 6
        else:
            newZoom = min(self.currentZoomOption+1, len(self.zoomOptions)-1)
        self.setZoom(newZoom)
        self.zoom_selector.setCurrentIndex(newZoom)
        pass
    
    def zoomOut(self):
        newZoom = 0
        if self.pdf_view.zoomMode() != QPdfView.ZoomMode.Custom:
            newZoom = 6
        else:
            newZoom = max(self.currentZoomOption-1, 2)
        self.setZoom(newZoom)
        self.zoom_selector.setCurrentIndex(newZoom)
        pass