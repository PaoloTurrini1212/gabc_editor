from PySide6.QtWidgets import (
    QApplication,
    #QMessageBox,
)
from PySide6.QtCore import QTranslator, QLocale, QLibraryInfo
from PySide6.QtCore import QCoreApplication, QSettings
import sys
#import os
from src.gabc_window import GabcWindow
#from src.latex_compile import compile_preview

app = QApplication(sys.argv)
app.setApplicationDisplayName("GABC Editor")

# Impostazioni / opzioni
QCoreApplication.setOrganizationName("GABC Editor")

# Imposta lingua
translator = QTranslator(app)
locale = QLocale.system().name()
print("locale ", locale)
translation_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
print("translation_path ", translation_path)
translator.load(f"qt_{locale}", translation_path)
app.installTranslator(translator)

# Controlli preliminari

# Imposta una categoria personalizzata per l'applicazione
# (permette di visualizzare un'icona personalizzata nella barra di Windows)
try:
    from ctypes import windll  # solo per Windows

    windll.shell32.SetCurrentProcessExplicitAppUserModelID("it.paolo.gabc_editor")
except ImportError:
    pass


# Controlla la presenza di LuaLaTeX e della libreria Gregorio
# Se non li trova, chiude il programma
#check_lualatex = os.system("cmd /c lualatex --version")
#check_gregorio = os.system("cmd /c gregorio --version")
#if check_lualatex > 0 or check_gregorio > 0:
#    lualatex_missing = (
#        """<p>Non è stato trovato il programma LuaLaTeX.<br>
#Questa risorsa è necessaria per compilare l'anteprima del file .gabc.<br>
#Controllare la propria distribuzione LaTeX ed eventualmente (re)installarla.<br>
#Per informazioni consulta il <a href="https://www.latex-project.org/get/">sito del Progetto LaTeX</a>.</p>"""
#        if check_lualatex > 0
#        else ""
#    )
#    gregorio_missing = (
#        """<p>Non è stato trovato il pacchetto Gregorio.<br>
#Questa risorsa è necessaria per compilare l'anteprima del file .gabc.<br>
#Installare il pacchetto seguendo le indicazioni sul <a href="http://gregorio-project.github.io/installation.html">sito del progetto Gregorio</a>."""
#        if check_gregorio > 0
#        else ""
#    )
#    error_text = "\n\n".join([lualatex_missing, gregorio_missing])
#    QMessageBox(QMessageBox.Icon.Critical, "Errore", error_text, parent=None).exec()
#    quit()


if __name__ == "__main__":
    w = GabcWindow()
    sys.exit(app.exec())
