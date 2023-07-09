import os
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMessageBox

def check_prerequisites(settings: QSettings):
    prerequisites_verified = settings.value("prerequisites_verified")
    if (prerequisites_verified != None and int(settings.value("prerequisites_verified")) == 1):
        return True

    # Controlla la presenza di LuaLaTeX e della libreria Gregorio
    # Se non li trova, chiude il programma
    check_lualatex = os.system("cmd /c lualatex --version")
    check_gregorio = os.system("cmd /c gregorio --version")
    if check_lualatex > 0 or check_gregorio > 0:
        lualatex_missing = (
            """<p>Non è stato trovato il programma LuaLaTeX.<br>
Questa risorsa è necessaria per compilare l'anteprima del file .gabc.<br>
Controllare la propria distribuzione LaTeX ed eventualmente (re)installarla.<br>
Per informazioni consulta il <a href="https://www.latex-project.org/get/">sito del Progetto LaTeX</a>.</p>"""
            if check_lualatex > 0
            else ""
        )
        gregorio_missing = (
            """<p>Non è stato trovato il pacchetto Gregorio.<br>
Questa risorsa è necessaria per compilare l'anteprima del file .gabc.<br>
Installare il pacchetto seguendo le indicazioni sul <a href="http://gregorio-project.github.io/installation.html">sito del progetto Gregorio</a>."""
            if check_gregorio > 0
            else ""
        )
        error_text = "\n\n".join([lualatex_missing, gregorio_missing])
        QMessageBox(QMessageBox.Icon.Critical, "Errore", error_text, parent=None).exec()
        settings.setValue("prerequisites_verified", 0)
        return False
    settings.setValue("prerequisites_verified", 1)
    return True