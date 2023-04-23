from PySide6.QtCore import QSettings, QSize, Qt, QThreadPool
from PySide6.QtGui import QColor, QFontDatabase, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (QApplication, QDockWidget, QFileDialog, QLabel,
                                QMainWindow, QMessageBox, QStatusBar, QStyle,
                                QTabWidget)

from src.editor import GabcEditor
from src.latex_compile import compile_preview
from src.logview import LogView
from src.pdf_preview import PdfPreview
from src.settings import SettingsDialog
from src.showinfo import showinfo
from src.snippets import SnippetInsert
from src.worker import Worker
from utils import baseName, relPath


# Applicazione principale
class GabcWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon(relPath("resources/icona_greg.ico")))
        self.settings = QSettings(relPath("config.ini"), QSettings.Format.IniFormat)
        
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

        # Contenitore a tab per gli editor

        self.editor_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        self.editor_font.setPointSize(12)

        self.editor_tabs = QTabWidget()
        self.editor_tabs.setMovable(True)
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.currentChanged.connect(self.current_tab_changed)
        self.editor_tabs.tabCloseRequested.connect(self.close_file)

        self.new_files_counter = 1
        # first_tab = GabcEditor(self, file="", font=self.editor_font)
        # self.editor_tabs.addTab(first_tab, f"nuovo{self.new_files_counter}.gabc")
        # first_tab.modificationChanged.connect(self.updateWindowTitle)
        self.setWindowTitle(f"nuovo{self.new_files_counter}.gabc[*]")
        self.getCurrentEditor().cursorPositionChanged.connect(self.updateLineMsg)

        # Logger

        self.logger_font = self.editor_font
        self.logger_font.setPointSize(10)

        self.logger = LogView(self)
        self.logger.setFont(self.logger_font)
        # debug
        """ with open("./resources/anteprima.log", "r", encoding="utf-8") as file:
            self.logger.add_log(file.read()) """

        # Anteprima

        self.preview_widget = PdfPreview(self)
        #self.preview_widget.loadPdf("resources/anteprima.pdf")

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
        left_dock = QDockWidget("Strumenti")
        self.char_map = SnippetInsert(left_dock)
        self.char_map.char_selected.connect(self.insertTextInCurrentEditor)
        left_dock.setWidget(self.char_map)
        left_dock.setObjectName("side_toolbar")
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, left_dock)

        # Azioni di menu e pulsanti

        newfile_action = self.addAction("Nuovo", "Ctrl+N")
        newfile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        )
        newfile_action.setStatusTip("Nuovo")
        newfile_action.triggered.connect(self.new_file)
        self.addAction(newfile_action)

        openfile_action = self.addAction("Apri", "Ctrl+O")
        openfile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        )
        openfile_action.setStatusTip("Apri")
        openfile_action.triggered.connect(self.open_file)

        savefile_action = self.addAction("Salva", "Ctrl+S")
        savefile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        )
        savefile_action.setStatusTip("Salva")
        savefile_action.triggered.connect(self.save_file)

        saveasfile_action = self.addAction("Salva con nome...", "Ctrl+Shift+S")
        saveasfile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DriveFDIcon)
        )
        saveasfile_action.setStatusTip("Salva con nome...")
        saveasfile_action.triggered.connect(self.save_as_file)

        compile_action = self.addAction("Compila", "Ctrl+P")
        compile_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
        )
        compile_action.setStatusTip("Compila (Ctrl+P)")
        compile_action.triggered.connect(self.start_compile_preview)

        export_action = self.addAction("Esporta...")
        export_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileLinkIcon)
        )
        export_action.setStatusTip("Esporta...")
        export_action.triggered.connect(self.export)
        
        settings_action = self.addAction("Impostazioni...")
        settings_action_icon = QIcon("resources/icona_opzioni.png")
        settings_action.setIcon(settings_action_icon)
        settings_action.setStatusTip("Impostazioni...")
        settings_action.triggered.connect(self.open_settings)

        help_action = self.addAction("Aiuto")
        help_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        )
        help_action.setStatusTip("Aiuto")
        help_action.triggered.connect(self.show_help)

        info_action = self.addAction("Informazioni su GabcEditor")
        info_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView)
        )
        info_action.setStatusTip("Informazioni su GabcEditor")
        info_action.triggered.connect(self.show_info)

        exit_action = self.addAction("&Esci")  # , "Alt+F4"
        exit_action.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton)
        )
        exit_action.setStatusTip("Esci")
        exit_action.triggered.connect(self.close_app)

        undo_action = self.addAction("Annulla", "Ctrl+Z")
        undo_action.setStatusTip("Annulla")
        undo_action.triggered.connect(self.getCurrentEditor().undo)

        redo_action = self.addAction("Ripristina", "Ctrl+Y")
        redo_action.setStatusTip("Ripristina")
        redo_action.triggered.connect(self.getCurrentEditor().redo)

        selectall_action = self.addAction("Seleziona tutto", "Ctrl+A")
        selectall_action.setStatusTip("Seleziona tutto")
        selectall_action.triggered.connect(self.getCurrentEditor().selectAll)

        cut_action = self.addAction("Taglia", "Ctrl+X")
        cut_action.setStatusTip("Taglia")
        cut_action.triggered.connect(self.getCurrentEditor().cut)

        copy_action = self.addAction("Copia", "Ctrl+C")
        copy_action.setStatusTip("Copia")
        copy_action.triggered.connect(self.getCurrentEditor().copy)

        paste_action = self.addAction("Incolla", "Ctrl+V")
        paste_action.setStatusTip("Incolla")
        paste_action.triggered.connect(self.getCurrentEditor().paste)

        # Menu

        self.menu = self.menuBar()

        file_menu = self.menu.addMenu("&File")
        file_menu.addAction(newfile_action)
        file_menu.addAction(openfile_action)
        file_menu.addAction(savefile_action)
        file_menu.addAction(saveasfile_action)
        file_menu.addSeparator()
        file_menu.addAction(export_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = self.menu.addMenu("&Modifica")
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(selectall_action)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        gabc_menu = self.menu.addMenu("&GABC")
        gabc_menu.addAction(compile_action)

        options_menu = self.menu.addMenu("Opzioni")
        options_menu.addAction(settings_action)

        help_menu = self.menu.addMenu("&?")
        help_menu.addAction(help_action)
        help_menu.addAction(info_action)

        # Toolbar
        self.toolbar = self.addToolBar("Strumenti")
        self.toolbar.setObjectName("main_toolbar")
        self.toolbar.addAction(newfile_action)
        self.toolbar.addAction(openfile_action)
        self.toolbar.addAction(savefile_action)
        self.toolbar.addAction(saveasfile_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(compile_action)
        self.toolbar.addAction(export_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(settings_action)

        geometry = self.settings.value("geometry")
        if geometry==None: geometry = self.saveGeometry()
        self.restoreGeometry(geometry)
        windowState = self.settings.value("windowState")
        if windowState==None: windowState = self.saveState()
        self.restoreState(windowState)
        
        self.show()
    
    def getCurrentEditor(self) -> GabcEditor:
        return (GabcEditor)(self.editor_tabs.currentWidget())
    
    def insertTextInCurrentEditor(self, text:str):
        self.getCurrentEditor().insertPlainText(text)
        self.getCurrentEditor().setFocus()
    
    def current_tab_changed(self, index):
        if index >= 0:
            self.getCurrentEditor().cursorPositionChanged.connect(self.updateLineMsg)
            filename = self.getCurrentEditor().file if self.getCurrentEditor().file else self.editor_tabs.tabText(index)
            #print(index, filename)
            self.setWindowTitle(filename+"[*]")
            self.updateWindowTitle()
            self.setWindowModified(self.getCurrentEditor().isWindowModified())
        pass

    # Aggiorna numero di riga e colonna
    def updateLineMsg(self, *args):
        pos = self.getCurrentEditor().textCursor()
        line_msg = f"Riga {pos.blockNumber()+1}, Colonna {pos.columnNumber()}"
        self.status_editor_pos.setText(line_msg)
    
    # Aggiorna titolo della finestra col nome del file
    def updateWindowTitle(self, *args):
        """ noneModified = True
        for i in range(self.editor_tabs.count()):
            if ((GabcEditor)(self.editor_tabs.widget(i)).document().isModified()):
                # almeno 1 file è modificato
                noneModified = False
                self.editor_tabs.setTabText(i, self.editor_tabs.tabText(i)+"*")
                pass
        # nessun file è modificato
        self.setWindowModified(noneModified) """
        pass

    # Gestione file

    # TODO: filename
    def new_file(self):
        self.new_files_counter += 1
        new_tab = GabcEditor(self, file="", font=self.editor_font)
        filename = f"nuovo{self.new_files_counter}.gabc"
        self.editor_tabs.addTab(new_tab, filename)
        self.editor_tabs.setCurrentWidget(new_tab)
        #self.logger.clear()
        self.setWindowTitle(filename+"[*]")
        new_tab.modificationChanged.connect(self.updateWindowTitle)
        self.preview_widget.clearPdf()
        #self.setWindowModified(False)
        pass

    # TODO: filename
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
            with open(self.getCurrentEditor().file, "r", encoding="utf-8") as file:
                self.getCurrentEditor().insertPlainText(file.read())
                new_tab = GabcEditor(self, file=fileName[0], font=self.editor_font)
                self.editor_tabs.addTab(new_tab, baseName(fileName[0]))
                self.editor_tabs.setCurrentWidget(new_tab)
                self.preview_widget.clearPdf()
                #self.getCurrentEditor().setWindowModified(False)
                #self.setWindowModified(False)
        except Exception as e:
            pass
        pass

    # TODO: filename
    def close_file(self, index):
        self.editor_tabs.setCurrentIndex(index)
        temp_title = self.editor_tabs.tabText(index)
        if not self.getCurrentEditor().isWindowModified():
            pass
        save_choice = QMessageBox.question(
            self,
            "Salva",
            f"Salvare il file {temp_title} ?",
            (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel),
            QMessageBox.StandardButton.Yes
        )
        if save_choice == QMessageBox.StandardButton.Cancel.value or save_choice == QMessageBox.StandardButton.Close.value:
            return
        if save_choice == QMessageBox.StandardButton.Yes.value:
            self.save_as_file()
        self.editor_tabs.removeTab(index)
        pass

    # TODO: filename
    def save_file(self):
        if self.getCurrentEditor().file == "":
            fileName = QFileDialog.getSaveFileName(
                self,
                "Salva file Gabc",
                self.settings.value("save_path"),
                filter="Notazione GABC (*.gabc)",
            )
            if fileName[0] == "":
                return
            self.getCurrentEditor().file = fileName[0]
        content = self.getCurrentEditor().toPlainText()
        with open(self.getCurrentEditor().file, "w", encoding="utf-8") as file:
            file.write(content)
        self.getCurrentEditor().setWindowModified(False)
        self.setWindowModified(False)
        pass

    # TODO: filename
    def save_as_file(self):
        fileName = QFileDialog.getSaveFileName(
            self, "Salva con nome", self.settings.value("save_path"), filter="Notazione GABC (*.gabc)"
        )
        if fileName[0] == "":
            return
        self.getCurrentEditor().file = fileName[0]
        content = self.getCurrentEditor().toPlainText()
        with open(self.getCurrentEditor().file, "w", encoding="utf-8") as file:
            file.write(content)
        self.getCurrentEditor().setWindowModified(False)
        self.setWindowModified(False)
        pass

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
    def export(self, export_type):
        #print("esporta", export_type)
        fileName = QFileDialog.getSaveFileName(
            self, "Salva file Gabc", self.settings.value("save_path"), filter="Immagine PNG (*.png);;Immagine JPEG (*.jpg)"
        )
        img = self.preview_widget.toQImage()
        img.save(fileName[0])
        pass

    def open_settings(self):
        SettingsDialog(self.settings, self).exec()
        pass

    # Aiuto

    def show_help(self):
        print("aiuto")
        pass

    def show_info(self):
        showinfo(self)
        pass

    def before_closing(self):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        for i in range(self.editor_tabs.count()):
            print(i, self.editor_tabs.tabText(i))
            self.close_file(i)
        pass

    def close_app(self):
        QApplication.instance().quit()
        pass