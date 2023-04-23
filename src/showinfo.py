from PySide6.QtWidgets import QMessageBox
from utils import relPath

def showinfo(parent):
    VERSION = "0.1.1"
    LICENSE_PATH = relPath("LICENSE.txt").replace('\\','/')
    #print(LICENSE_PATH)
    text = f""" <h1>GABC Editor</h1>
    <p>Versione {VERSION}</p>
    <p>(C) 2023 Paolo Turrini</p>
    <p>Rilasciato con <a href="{LICENSE_PATH}">licenza MIT</a></p>
    <br>
    <p>Il programma è scritto in Python e si basa sulla libreria <a href="https://www.qt.io/qt-for-python">PySide (Qt for Python)</a>,
    rilasciata con <a href="https://www.gnu.org/licenses/lgpl-3.0.html">licenza LGPL</a>.</p> """
    QMessageBox(QMessageBox.Icon.Information, "Informazioni su GABC Editor", text, parent=parent).exec()