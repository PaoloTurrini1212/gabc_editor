from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QColor, QTextCharFormat
from .syntax_highlighter import Highlighter

# Casella di testo per visualizzare i log di compilazione


class LogView(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self._process = QProcess()
        self._process.readyReadStandardOutput.connect(self.handle_stdout)
        self._process.readyReadStandardError.connect(self.handle_stderr)

        # Evidenziatore sintassi

        mappings = {}

        pattern_error = r"[eE]rror"
        fmt_error = QTextCharFormat()
        fmt_error.setFontWeight(900)
        fmt_error.setForeground(QColor("#dd0000"))
        mappings[pattern_error] = fmt_error

        pattern_warning = r"[wW]arning"
        fmt_warning = QTextCharFormat()
        fmt_warning.setFontWeight(900)
        fmt_warning.setForeground(QColor("#ffbb00"))
        mappings[pattern_warning] = fmt_warning

        pattern_ok = r"Output written on .+"
        fmt_ok = QTextCharFormat()
        fmt_ok.setFontWeight(900)
        fmt_ok.setForeground(QColor("#00dd00"))
        mappings[pattern_ok] = fmt_ok

        pattern_info = r"[iI]nfo"
        fmt_info = QTextCharFormat()
        fmt_info.setFontWeight(900)
        fmt_info.setForeground(QColor("#000088"))
        mappings[pattern_info] = fmt_info

        self.highlighter = Highlighter(self)
        self.highlighter.setMappings(mappings)
        self.highlighter.setDocument(self.document())

    def start_log(self, program, arguments=None):
        if arguments is None:
            arguments = []
        self._process.start(program, arguments)

    def add_log(self, message):
        self.appendPlainText(message.rstrip())

    def handle_stdout(self):
        message = self._process.readAllStandardOutput().data().decode()
        self.add_log(message)

    def handle_stderr(self):
        message = self._process.readAllStandardError().data().decode()
        self.add_log(message)
