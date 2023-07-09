from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QScrollArea, QGridLayout, QVBoxLayout, QPushButton, QButtonGroup, QLabel

# Unicode:  https://unicodeplus.com/
# Simboli musicali: 1d100 - 1d1ff
# Misc:  U+1F300 - U+1F5FF
# Unicode 32-bit: \U12345678 (U maiuscola, 8 caratteri)

# SnippetInsert
class SnippetInsert(QWidget):
    chars = [
        ("`", "`", "backtick"),
        ("~", "~", "tilde"),
        ("\u00e1", r"<v>{\'a}</v>", "a minuscola accentata"),
        ("é", r"<v>{\'e}</v>", "e minuscola accentata"),
        ("\u00ed", r"<v>{\'i}</v>", "i minuscola accentata"),
        ("\u00f3", r"<v>{\'o}</v>", "o minuscola accentata"),
        ("\u00fa", r"<v>{\'u}</v>", "u minuscola accentata"),
        ("\u00fd", r"<v>{\'y}</v>", "y minuscola accentata"),
        ("\u00e6", r"<v>{\ae}</v>", "legatura ae minuscola"),
        ("\u01fd", r"<v>{\'\ae}</v>", "legatura ae minuscola accentata"),
        ("\u0153", r"<v>{\oe}</v>", "legatura oe minuscola"),
        ("\u0153\u0301", r"<v>{\'\oe}</v>", "legatura oe minuscola accentata"),
        ("\u00c1", r"<v>{\'A}</v>", "A maiuscola accentata"),
        ("\u00c9", r"<v>{\'E}</v>", "E maiuscola accentata"),
        ("\u00cd", r"<v>{\'I}</v>", "I maiuscola accentata"),
        ("\u00d3", r"<v>{\'O}</v>", "O maiuscola accentata"),
        ("\u00da", r"<v>{\'U}</v>", "U maiuscola accentata"),
        ("\u00dd", r"<v>{\'Y}</v>", "Y maiuscola accentata"),
        ("\u00c6", r"<v>{\AE}</v>", "legatura AE maiuscola"),
        ("\u01fc", r"<v>{\'\AE}</v>", "legatura AE maiuscola accentata"),
        ("\u0152", r"<v>{\OE}</v>", "legatura OE maiuscola"),
        ("\u0152\u0301", r"<v>{\'\OE}</v>", "legatura OE maiuscola accentata"),
        ("\u2123", r"<sp>V/</sp>", "versetto"),
        ("\u211f", r"<sp>R/</sp>", "risposta"),
        ("\u023a", r"<sp>A/</sp>", "antifona"),
        # ("V/", r"<sp>\gothVbar</sp>", "versetto (V gotica)"),
        # ("R/", r"<sp>\gothRbar</sp>", "risposta (R gotica)"),
        ("\u2720", r"<sp>\grecross</sp>", "croce"),
        ("\u2629", r"<sp>\grealtcross</sp>", "croce (alt.)"),
        ("\u2020", "<v>\dag</v>", "croce latina"),
        ("\u204e", r"<sp>\greheightstar</sp>", "asterisco (8 punte)"),
        ("\u273d", r"<sp>\gresixstar</sp>", "asterisco (6 punte)"),
    ]
    snippets = [
        ("Base", "name: test;\n%%\n(c2) A(f)", "Template minimo GABC"),
        ("Con header", "name: test;\nmode: 1;\nmode-modifier: a;\nmode-differentia: d;\ndate: XI sec.;\ngabc-copyright: CC0-1.0 by Elie Roux, 2009 <http://creativecommons.org/publicdomain/zero/1.0/>;\ncommentary: commento;\n%%\n(c2) A(f)men.(fg.) (::)", "Template GABC con le opzioni più comuni nell'header"),
    ]
    char_selected = Signal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())
        self.scroll_area = QScrollArea()
        self.scroll_area.setLayout(QVBoxLayout())
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout().setContentsMargins(1,1,1,1)
        self.layout().addWidget(self.scroll_area)
        self.container = QWidget()
        self.container.setLayout(QVBoxLayout())
        self.container.setStyleSheet("QPushButton { font-size: 16px; background-color: #fafff5; border: 1px solid #003; margin: 1px; padding: 1px; border-radius: 2px; } QButtonGroup { border: 1px solid #333; padding: 1px; } QLabel { font-weight: bold; border-top: 1px solid #444; padding-top: 1px; margin-top: 2px; }")

        self.char_grid = QWidget()
        self.char_grid.setLayout(QGridLayout())
        self.char_grid.layout().setSpacing(0)
        self.char_grid.layout().setContentsMargins(0,0,0,0)
        self.container.layout().addWidget(QLabel("Caratteri speciali"))
        self.container.layout().addWidget(self.char_grid)

        self.char_cols = 5
        self.char_btn_w = 40

        self.snippet_grid = QWidget()
        self.snippet_grid.setLayout(QVBoxLayout())
        self.snippet_grid.layout().setContentsMargins(1,1,1,1)
        self.container.layout().addWidget(QLabel("Modelli preimpostati"))
        self.container.layout().addWidget(self.snippet_grid)

        self.char_btns = QButtonGroup()
        self.char_btns.idClicked.connect(self.sendCharToTextEditor)
        for i, char in enumerate(self.chars):
            button = QPushButton(char[0], objectName=f"char_{i}")
            button.setToolTip(char[2])
            button.setMaximumWidth(self.char_btn_w)
            self.char_btns.addButton(button, i)
            self.char_grid.layout().addWidget(button, int(i/self.char_cols), i % self.char_cols)
        
        self.snippet_btns = QButtonGroup()
        self.snippet_btns.idClicked.connect(self.sendSnippetToTextEditor)
        for i, snippet in enumerate(self.snippets):
            button = QPushButton(snippet[0], objectName=f"snippet_{i}")
            button.setToolTip(snippet[2])
            button.setStyleSheet("background-color: #faef75;")
            self.snippet_btns.addButton(button, i)
            self.snippet_grid.layout().addWidget(button)
        
        #self.setMinimumWidth(self.sizeHint().width())
        self.scroll_area.setWidget(self.container)
        self.scroll_area.show()
    
    def sendCharToTextEditor(self, id):
        self.char_selected.emit(self.chars[id][1])

    def sendSnippetToTextEditor(self, id):
        self.char_selected.emit(self.snippets[id][1])