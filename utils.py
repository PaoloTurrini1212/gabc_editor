import os

# Utilità per i path relativi

ROOT_PATH = os.path.dirname(__file__)


def relPath(path):
    return os.path.join(ROOT_PATH, path)

def baseName(path):
    return os.path.basename(path)


# Finestra di progresso generica
""" class ProgressDialog(QDialog):
    def __init__(self, parent=None, text=""):
        super().__init__(parent)
        self.text = text
        self.setWindowTitle("Operazione in corso...")
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.label = QLabel("")
        self.layout.addWidget(self.label)
        #self.setWindowFlags(Qt.w)

    def setText(self, text):
        self.text = text """
