from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtWidgets import QWidget, QPlainTextEdit
from PySide6.QtGui import QPainter, QPaintEvent, QColor, QTextCharFormat
from .syntax_highlighter import Highlighter

# Editor di codice Gabc (con numeri di riga ed evidenziatore di sintassi)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setFont(editor.font())

    def sizeHint(self) -> QSize:
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, e: QPaintEvent):
        return self.editor.lineNumberAreaPaintEvent(e)


class GabcEditor(QPlainTextEdit):
    def __init__(self, parent=None, file="", font=None):
        super().__init__(parent)
        self.file = file
        if font:
            self.setFont(font)

        # self.textChanged.connect(self.debugText)
        
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)

        # Evidenziatore sintassi

        mappings = {}

        pattern_brackets = r"[\(\)]+"
        fmt_brackets = QTextCharFormat()
        fmt_brackets.setFontWeight(900)
        fmt_brackets.setForeground(QColor("#ff00ff"))
        mappings[pattern_brackets] = fmt_brackets

        pattern_comment = r"%.*"  # %.*(?=[\t\n\r])
        fmt_comment = QTextCharFormat()
        fmt_comment.setFontItalic(True)
        fmt_comment.setForeground(QColor("#888888"))
        mappings[pattern_comment] = fmt_comment

        pattern_header = r"[\w\-]+(?=:)"
        fmt_header = QTextCharFormat()
        fmt_header.setForeground(QColor("#882200"))
        mappings[pattern_header] = fmt_header

        # pattern_header_semicolon = r"[;]+(?=[\s]*[\t\n\r])"
        # fmt_header_semicolon = QTextCharFormat()
        # fmt_header_semicolon.setForeground(QColor("#00aa00"))
        # mappings[pattern_header_semicolon] = fmt_header_semicolon

        pattern_neume = r"(?<=\()[^\(\)]+(?=\))"
        fmt_neume = QTextCharFormat()
        fmt_neume.setForeground(QColor("#0000aa"))
        mappings[pattern_neume] = fmt_neume

        """ pattern_pitch = r"(?<=\([^\(\)]*)[a-m](?=[^\(\)]*\))"
        fmt_pitch = QTextCharFormat()
        fmt_pitch.setForeground(QColor("#0000aa"))
        mappings[pattern_pitch] = fmt_pitch """

        pattern_tag = r"\<\/?[\w\-\_]+\>"
        fmt_tag = QTextCharFormat()
        fmt_tag.setForeground(QColor("#338800"))
        mappings[pattern_tag] = fmt_tag

        pattern_escape = r"[$]{1}.{1}"
        fmt_escape = QTextCharFormat()
        fmt_escape.setForeground(QColor("#00aaaa"))
        mappings[pattern_escape] = fmt_escape

        self.highlighter = Highlighter(self)
        self.highlighter.setMappings(mappings)
        self.highlighter.setDocument(self.document())
        pass

    def isTextModified(self):
        return self.document().isModified()

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().maxWidth() * digits
        return space

    def updateLineNumberAreaWidth(self, *args):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(
                0, rect.y(), self.lineNumberArea.width(), rect.height()
            )
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        mypainter = QPainter(self.lineNumberArea)

        mypainter.fillRect(event.rect(), QColor("#ddeeff"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = int(top + self.blockBoundingRect(block).height())

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(QColor("#6666aa"))
                mypainter.drawText(
                    0, top, self.lineNumberArea.width(), height, Qt.AlignmentFlag.AlignRight, number
                )

            block = block.next()
            top = bottom
            bottom = int(top + self.blockBoundingRect(block).height())
            blockNumber += 1
