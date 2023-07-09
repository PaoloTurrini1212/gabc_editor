from PySide6.QtCore import QSettings, QSize, Qt, QThreadPool
from PySide6.QtGui import QColor, QFontDatabase, QIcon, QPainter, QPixmap, QKeySequence
from PySide6.QtWidgets import (QApplication, QDockWidget, QFileDialog, QLabel,
                                QMainWindow, QMessageBox, QStatusBar, QStyle,
                                QTabWidget)

from src.editor import GabcEditor
from src.latex_compile import compile_preview
from src.logview import LogView
from src.pdf_preview import PdfPreview
from src.settings import SettingsDialog
from src.help_window import HelpWindow
from src.showinfo import showinfo
from src.snippets import SnippetInsert
from src.worker import Worker
from src.export_type_selector import ExportTypeSelector, export_types
from utils import baseName, relPath
from shutil import copyfile


# Applicazione principale
class GabcWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings(relPath("config.ini"), QSettings.Format.IniFormat)
        self.prerequisites_verified = self.settings.value("prerequisites_verified")
        if self.prerequisites_verified is None:
            self.prerequisites_verified = 0
        self.initUI()
    
    # *******
    #  SETUP
    # *******

    def initUI(self):
        self.setWindowIcon(QIcon(relPath("resources/icona_greg.ico")))
        
        self.status_font = QFontDatabase.systemFont(
            QFontDatabase.SystemFont.GeneralFont
        )
        self.status_font.setPointSize(12)

        # Barra di stato

        self.status_bar = QStatusBar(self)
        self.status_bar.setFont(self.status_font)
        self.setStatusBar(self.status_bar)

        self.status_editor_pos = QLabel()
        self.status_msg = QLabel()
        self.status_bar.addPermanentWidget(self.status_msg, 1)
        self.status_bar.addPermanentWidget(self.status_editor_pos, 0)

        # Threadpool

        self.threadpool = QThreadPool()

        # Riquadro anteprima pdf

        self.preview_widget = PdfPreview(self)

        # Contenitore a tab per gli editor

        self.newfile_count = 1

        self.editor_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        self.editor_font.setPointSize(12)

        self.editor_tabs = QTabWidget()
        self.editor_tabs.setDocumentMode(True)
        self.editor_tabs.setMovable(True)
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.currentChanged.connect(self.current_tab_changed)
        self.editor_tabs.tabCloseRequested.connect(self.close_file)
        self.new_file()

        # Logger

        self.logger_font = self.editor_font.__copy__()
        self.logger_font.setPointSize(10)

        self.logger = LogView(self)
        self.logger.setFont(self.logger_font)
        # debug
        """ with open("./resources/anteprima.log", "r", encoding="utf-8") as file:
            self.logger.add_log(file.read()) """

        # Layout

        self.setCentralWidget(self.editor_tabs)
        right_dock = QDockWidget("Anteprima PDF")
        right_dock.setWidget(self.preview_widget)
        right_dock.setObjectName("pdf_preview")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, right_dock)

        bottom_dock = QDockWidget("Messaggi di compilazione")
        bottom_dock.setWidget(self.logger)
        bottom_dock.setObjectName("logger")
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, bottom_dock)

        # TODO: sidebar con tool multipli
        left_dock = QDockWidget("Inserimento veloce")
        self.char_map = SnippetInsert(left_dock)
        self.char_map.char_selected.connect(self.insertTextInCurrentEditor)
        left_dock.setWidget(self.char_map)
        left_dock.setObjectName("side_toolbar")
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, left_dock)

        # Crea azioni, menu e barra strumenti
        self.initMenu()

        # Operazioni di caricamento
        geometry = self.settings.value("geometry")
        if geometry==None: geometry = self.saveGeometry()
        self.restoreGeometry(geometry)
        windowState = self.settings.value("windowState")
        if windowState==None: windowState = self.saveState()
        self.restoreState(windowState)
        
        self.show()
    
    def initMenu(self):
        # Azioni di menu e pulsanti

        self.newfile_action = self.addAction("Nuovo", QKeySequence.StandardKey.New)
        self.newfile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        )
        self.newfile_action.setStatusTip("Nuovo")
        self.newfile_action.triggered.connect(self.new_file)

        self.openfile_action = self.addAction("Apri", QKeySequence.StandardKey.Open)
        self.openfile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        )
        self.openfile_action.setStatusTip("Apri")
        self.openfile_action.triggered.connect(self.open_file)

        self.savefile_action = self.addAction("Salva", QKeySequence.StandardKey.Save)
        self.savefile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        )
        self.savefile_action.setStatusTip("Salva")
        self.savefile_action.triggered.connect(self.save_file)

        self.saveasfile_action = self.addAction("Salva con nome...", "Ctrl+Shift+S")
        self.saveasfile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DriveFDIcon)
        )
        self.saveasfile_action.setStatusTip("Salva con nome...")
        self.saveasfile_action.triggered.connect(self.save_as_file)

        self.compile_action = self.addAction("Compila", "Ctrl+Enter")
        self.compile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
        )
        self.compile_action.setStatusTip("Compila (Ctrl+Enter)")

        self.export_action = self.addAction("Esporta...")
        self.export_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileLinkIcon)
        )
        self.export_action.setStatusTip("Esporta...")

        if (self.prerequisites_verified == 1):
            self.compile_action.triggered.connect(self.start_compile_preview)
            self.export_action.triggered.connect(self.export)
        else:
            self.compile_action.setEnabled(False)
            self.export_action.setEnabled(False)
            self.compile_action.setToolTip("Compila (funzione disabilitata)")
            self.export_action.setToolTip("Esporta (funzione disabilitata)")
        
        self.settings_action = self.addAction("Impostazioni...")
        settings_action_icon = QIcon("resources/icona_opzioni.png")
        self.settings_action.setIcon(settings_action_icon)
        self.settings_action.setStatusTip("Impostazioni...")
        self.settings_action.triggered.connect(self.open_settings)

        self.help_action = self.addAction("Aiuto")
        self.help_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        )
        self.help_action.setStatusTip("Aiuto")
        self.help_action.triggered.connect(self.show_help)

        self.info_action = self.addAction("Informazioni su GabcEditor")
        self.info_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView)
        )
        self.info_action.setStatusTip("Informazioni su GabcEditor")
        self.info_action.triggered.connect(self.show_info)

        self.exit_action = self.addAction("&Esci")  # , "Alt+F4"
        self.exit_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton)
        )
        self.exit_action.setStatusTip("Esci")
        self.exit_action.triggered.connect(self.close)

        self.undo_action = self.addAction("Annulla", "Ctrl+Z")
        self.undo_action.setStatusTip("Annulla")
        self.undo_action.triggered.connect(self.getCurrentEditor().undo)

        self.redo_action = self.addAction("Ripristina", "Ctrl+Y")
        self.redo_action.setStatusTip("Ripristina")
        self.redo_action.triggered.connect(self.getCurrentEditor().redo)

        self.selectall_action = self.addAction("Seleziona tutto", "Ctrl+A")
        self.selectall_action.setStatusTip("Seleziona tutto")
        self.selectall_action.triggered.connect(self.getCurrentEditor().selectAll)

        self.cut_action = self.addAction("Taglia", "Ctrl+X")
        self.cut_action.setStatusTip("Taglia")
        self.cut_action.triggered.connect(self.getCurrentEditor().cut)

        self.copy_action = self.addAction("Copia", "Ctrl+C")
        self.copy_action.setStatusTip("Copia")
        self.copy_action.triggered.connect(self.getCurrentEditor().copy)

        self.paste_action = self.addAction("Incolla", "Ctrl+V")
        self.paste_action.setStatusTip("Incolla")
        self.paste_action.triggered.connect(self.getCurrentEditor().paste)

        # Menu

        self.menu = self.menuBar()

        file_menu = self.menu.addMenu("&File")
        file_menu.addAction(self.newfile_action)
        file_menu.addAction(self.openfile_action)
        file_menu.addAction(self.savefile_action)
        file_menu.addAction(self.saveasfile_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = self.menu.addMenu("&Modifica")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.selectall_action)
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)

        gabc_menu = self.menu.addMenu("&GABC")
        gabc_menu.addAction(self.compile_action)

        options_menu = self.menu.addMenu("Opzioni")
        options_menu.addAction(self.settings_action)

        help_menu = self.menu.addMenu("&Aiuto")
        help_menu.addAction(self.help_action)
        help_menu.addAction(self.info_action)

        # Toolbar
        self.toolbar = self.addToolBar("Strumenti")
        self.toolbar.setObjectName("main_toolbar")
        self.toolbar.addAction(self.newfile_action)
        self.toolbar.addAction(self.openfile_action)
        self.toolbar.addAction(self.savefile_action)
        self.toolbar.addAction(self.saveasfile_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.compile_action)
        self.toolbar.addAction(self.export_action)
        # self.toolbar.addSeparator()
        # self.toolbar.addAction(self.settings_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.help_action)
        pass

    # ********
    #  METODI
    # ********

    def getCurrentEditor(self) -> GabcEditor:
        if self.editor_tabs.count() == 0:
            return None
        return self.editor_tabs.currentWidget()
    
    def insertTextInCurrentEditor(self, text:str):
        self.getCurrentEditor().insertPlainText(text)
        self.getCurrentEditor().setFocus()
        pass
    
    def current_tab_changed(self, index):
        if index >= 0 and index < self.editor_tabs.count():
            filename = self.getCurrentEditor().file if self.getCurrentEditor().file else self.editor_tabs.tabText(index)
            self.setWindowTitle(filename+"[*]")
            self.updateWindowTitle()
            self.setWindowModified(self.getCurrentEditor().isTextModified())
            self.updateLineMsg()
        pass

    # Aggiorna numero di riga e colonna
    def updateLineMsg(self, *args):
        pos = self.getCurrentEditor().textCursor()
        line_msg = f"Riga {pos.blockNumber()+1}, Colonna {pos.columnNumber()}"
        self.status_editor_pos.setText(line_msg)
        pass
    
    # Aggiorna titolo della finestra col nome del file
    def updateWindowTitle(self, *args):
        modified = False
        for i in range(self.editor_tabs.count()):
            if ((self.editor_tabs.widget(i)).isTextModified()):
                # almeno 1 file è modificato
                modified = True
                #self.editor_tabs.setTabText(i, self.editor_tabs.tabText(i)+"*")
                pass
        # nessun file è modificato
        self.setWindowModified(modified)
        pass

    def set_enabled_file_actions(self, enabled):
        if not hasattr(self, "savefile_action"):
            return
        self.savefile_action.setEnabled(enabled)
        self.saveasfile_action.setEnabled(enabled)
        self.compile_action.setEnabled(enabled)
        self.export_action.setEnabled(enabled)
        self.undo_action.setEnabled(enabled)
        self.redo_action.setEnabled(enabled)
        self.selectall_action.setEnabled(enabled)
        self.cut_action.setEnabled(enabled)
        self.copy_action.setEnabled(enabled)
        self.paste_action.setEnabled(enabled)
        pass

    def dialog_error(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
        pass

    # Gestione file

    def new_tab(self, fileName="", text="", tabName=""):
        tab = GabcEditor(self, file=fileName, font=self.editor_font)
        self.editor_tabs.addTab(tab, tabName)
        self.editor_tabs.setCurrentWidget(tab)
        tab.modificationChanged.connect(self.updateWindowTitle)
        self.setWindowTitle(f"{tabName}[*]")
        self.insertTextInCurrentEditor(text)
        self.getCurrentEditor().cursorPositionChanged.connect(self.updateLineMsg)
        self.preview_widget.clearPdf()
        self.set_enabled_file_actions(True)
        pass

    def new_file(self):
        self.new_tab("", "", f"Nuovo {self.newfile_count}.gabc")
        self.newfile_count += 1
        pass

    def open_file(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            "Apri file Gabc",
            self.settings.value("save_path"),
            filter="Notazione GABC (*.gabc);;Documenti di testo (*.txt)",
            selectedFilter="Notazione GABC (*.gabc)",
        )
        if fileName[0] == "":
            return
        try:
            with open(fileName, "r", encoding="utf-8") as file:
                text = file.read()
                self.new_tab(fileName, text, fileName)
        except Exception as e:
            self.dialog_error(e)
        pass

    def close_file(self, index):
        self.editor_tabs.setCurrentIndex(index)
        if self.getCurrentEditor().isTextModified():
            temp_title = self.editor_tabs.tabText(index)
            save_choice = QMessageBox.question(
                self,
                "Salva",
                f"Salvare il file {temp_title} ?",
                (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel),
                QMessageBox.StandardButton.Yes
            )
            if save_choice == QMessageBox.StandardButton.Cancel.value or save_choice == QMessageBox.StandardButton.Close.value:
                return False
            if save_choice == QMessageBox.StandardButton.Yes.value:
                saved = self.save_file()
                if not saved:
                    return False
        self.editor_tabs.removeTab(index)
        if self.editor_tabs.count() == 0:
            self.setWindowTitle("")
            self.set_enabled_file_actions(False)
        return True

    def save_file(self):
        if self.getCurrentEditor().file == "":
            fileName = QFileDialog.getSaveFileName(
                self,
                "Salva file Gabc",
                self.settings.value("save_path"),
                filter="Notazione GABC (*.gabc)",
            )
            if fileName[0] == "":
                return False
            self.getCurrentEditor().file = fileName[0]
            self.editor_tabs.setTabText(self.editor_tabs.currentIndex(), self.getCurrentEditor().file)
        content = self.getCurrentEditor().toPlainText()
        with open(self.getCurrentEditor().file, "w", encoding="utf-8") as file:
            file.write(content)
        self.getCurrentEditor().setWindowModified(False)
        self.setWindowModified(False)
        return True

    def save_as_file(self):
        fileName = QFileDialog.getSaveFileName(
            self, "Salva con nome", self.settings.value("save_path"), filter="Notazione GABC (*.gabc)"
        )
        if fileName[0] == "":
            return False
        self.getCurrentEditor().file = fileName[0]
        self.editor_tabs.setTabText(self.editor_tabs.currentIndex(), self.getCurrentEditor().file)
        content = self.getCurrentEditor().toPlainText()
        with open(self.getCurrentEditor().file, "w", encoding="utf-8") as file:
            file.write(content)
        self.getCurrentEditor().setWindowModified(False)
        self.setWindowModified(False)
        return True

    # Funzioni di compilazione LaTeX+Gregorio

    def start_compile_preview(self):
        [a.setEnabled(False) for a in self.actions()]
        gabc = self.getCurrentEditor().toPlainText()
        self.logger.clear()
        # Avvia compilazione pdf in un thread separato e collega gli eventi agli appositi metodi
        worker = Worker(compile_preview, gabc)
        worker.signals.error.connect(self.thread_error)
        worker.signals.partial.connect(self.thread_partial_result)
        worker.signals.result.connect(self.finished_compile_preview)
        worker.signals.finished.connect(self.thread_finished)
        self.threadpool.start(worker)
        # Apri finestra di attesa per impedire interazioni col programma
        # self.progressDialog.exec()
        pass

    def thread_partial_result(self, result):
        if result[0] != None:
            self.status_msg.setText(result[0])
        elif result[1] != None:
            self.logger.add_log(result[1])
        pass

    def thread_error(self, error):
        [a.setEnabled(True) for a in self.actions()]
        with open("./resources/anteprima.log", "r", encoding="utf-8") as file:
            self.logger.add_log(file.read())
        self.status_msg.setText("Errore")
        """ err_msg = QMessageBox(
            QMessageBox.Icon.Critical, "Errore", f"{error}", parent=self
        )
        err_msg.exec() """
        pass

    def thread_finished(self):
        pass

    def finished_compile_preview(self):
        self.preview_widget.loadPdf("./resources/anteprima.pdf")
        [a.setEnabled(True) for a in self.actions()]
        with open("./resources/anteprima.log", "r", encoding="utf-8") as file:
            self.logger.add_log(file.read())
        self.status_msg.setText("Operazione terminata.")
        pass

    # Esporta (con opzioni)
    def export(self):
        exportDialog = ExportTypeSelector(self)
        exportDialog.exec()
        export_type = exportDialog.selected_format
        filterStr = export_types[export_type]
        fileName = QFileDialog.getSaveFileName(self, "Esporta file Gabc", self.settings.value("save_path"), filter=filterStr)
        if (export_type == "png" or export_type == "jpg"):
            img = self.preview_widget.toQImage()
            img.save(fileName[0])
        elif (export_type == "tex" or export_type == "pdf"):
            copyfile(f"./resources/anteprima.{export_type}", fileName[0])
            pass
        pass

    # Impostazioni

    def open_settings(self):
        SettingsDialog(self.settings, self).exec()
        pass

    # Aiuto

    def show_help(self):
        self.helpWindow = HelpWindow(None, self.settings)
        self.helpWindow.show()
        pass

    def show_info(self):
        showinfo(self)
        pass

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        for i in range(self.editor_tabs.count()):
            file_closed = self.close_file(i)
            if not file_closed:
                event.ignore()
                return
        #QApplication.instance().quit()
        event.accept()