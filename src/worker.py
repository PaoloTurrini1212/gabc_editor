import sys
import traceback
from PySide6.QtCore import QObject, QRunnable, Signal, Slot # pyqtSignal, pyqtSlot

# Classi di utilità per avviare thread paralleli


class WorkerSignals(QObject):
    error = Signal(tuple)
    result = Signal(object)
    partial = Signal(object)
    finished = Signal()


class Worker(QRunnable):
    def __init__(self, callback, *args, **kwargs):
        super(Worker, self).__init__()
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            result = self.callback(self.signals, *self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()
