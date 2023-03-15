from typing import Dict
import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat #, QColor

# Evidenziatore di sintassi


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        QSyntaxHighlighter.__init__(self, parent)
        self._mappings = {}

    def setMappings(self, mappings: Dict[str, QTextCharFormat]):
        self._mappings = mappings
        pass

    def highlightBlock(self, text):
        for pattern, format in self._mappings.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, format)
