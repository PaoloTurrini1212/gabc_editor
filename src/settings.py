from PySide6.QtWidgets import QDialog, QFileDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import QSettings

class SettingsDialog(QDialog):
    def __init__(self, settings: QSettings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Opzioni")
        self.settings = settings
        
        self.save_path = QLineEdit(self.settings.value("save_path"))
        btn_save_path_browse = QPushButton("Seleziona...")
        btn_save_path_browse.clicked.connect(
            lambda: self.save_path.setText(
                QFileDialog.getExistingDirectory(
                    self,
                    "Seleziona cartella per il salvataggio",
                    self.settings.value("save_path")
                ) or self.settings.value("save_path")))
        row_save_path = QHBoxLayout()
        row_save_path.addWidget(self.save_path)
        row_save_path.addWidget(btn_save_path_browse)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.apply)
        self.buttonBox.rejected.connect(self.cancel)

        formLayout = QFormLayout()
        self.setLayout(formLayout)

        formLayout.addRow("Salva file in: ",  row_save_path)
        formLayout.addWidget(self.buttonBox)
    
    def apply(self):
        self.settings.setValue("save_path", self.save_path.text())
        self.accept()
        pass

    def cancel(self):
        self.reject()
        pass