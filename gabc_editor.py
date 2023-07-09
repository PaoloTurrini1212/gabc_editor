# coding=utf-8

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLocale, QLibraryInfo
from PySide6.QtCore import QCoreApplication, QSettings
import sys
from src.check_prerequisites import check_prerequisites
from src.gabc_window import GabcWindow
from utils import relPath

app = QApplication(sys.argv)
app.setApplicationDisplayName("GABC Editor")

# Impostazioni / opzioni
QCoreApplication.setOrganizationName("GABC Editor")

# Imposta lingua
translator = QTranslator(app)
locale = QLocale.system().name()
translation_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
translator.load("qt_{locale}", translation_path)
app.installTranslator(translator)

# Controlli preliminari

# Imposta una categoria personalizzata per l'applicazione
# (permette di visualizzare un'icona personalizzata nella barra di Windows)
try:
    from ctypes import windll  # solo per Windows

    windll.shell32.SetCurrentProcessExplicitAppUserModelID("it.paolo.gabc_editor")
except ImportError:
    pass

settings = QSettings(relPath("config.ini"), QSettings.Format.IniFormat)
check_prerequisites(settings)

if __name__ == "__main__":
    w = GabcWindow()
    sys.exit(app.exec())
