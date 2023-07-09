from PySide6.QtWidgets import QDialog, QButtonGroup, QVBoxLayout, QDialogButtonBox, QRadioButton

# TODO: selezione formato x export

export_types = {
    "pdf": "Documento PDF (*.pdf)",
    "tex": "Documento LaTeX (*.tex)",
    "png": "Immagine PNG (*.png)",
    "jpg": "Immagine JPEG (*.jpg)",
}

class ExportTypeSelector(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Esporta partitura")
        self.selected_format = ""

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.export_type_btns = QButtonGroup(self)

        self.type_pdf = QRadioButton(export_types["pdf"], self)
        self.type_tex = QRadioButton(export_types["tex"], self)
        self.type_png = QRadioButton(export_types["png"], self)
        self.type_jpg = QRadioButton(export_types["jpg"], self)

        self.export_type_btns.addButton(self.type_pdf)
        self.export_type_btns.addButton(self.type_tex)
        self.export_type_btns.addButton(self.type_png)
        self.export_type_btns.addButton(self.type_jpg)
        layout.addWidget(self.type_pdf)
        layout.addWidget(self.type_tex)
        layout.addWidget(self.type_png)
        layout.addWidget(self.type_jpg)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.apply)
        self.buttonBox.rejected.connect(self.cancel)
        layout.addWidget(self.buttonBox)
        pass
    
    def apply(self):
        self.selected_format = "pdf" if self.type_pdf.isChecked() else "tex" if self.type_tex.isChecked() else "png" if self.type_png.isChecked() else "jpg" if self.type_jpg.isChecked() else None
        self.accept()
        pass

    def cancel(self):
        self.reject()
        pass