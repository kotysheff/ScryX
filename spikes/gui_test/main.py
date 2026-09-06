import sys
import os
import time
import random
from PySide6.QtGui import QGuiApplication, QSurfaceFormat
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot, QThread
from PySide6.QtQuickControls2 import QQuickStyle

class MatrixWorker(QThread):
    data_received = Signal(str, float)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        core_names = ["ALPHA", "NEBULA", "QUANTUM", "CYPHER"]
        progress = 0.0
        while self.running and progress < 100.0:
            time.sleep(0.04)
            progress += random.uniform(0.8, 2.0)
            core = random.choice(core_names)
            hex_data = f"[{core}] Synced Block: 0x{random.randint(0x1000, 0xFFFF):X}..."
            self.data_received.emit(hex_data, min(progress, 100.0))

class UIBackend(QObject):
    logChanged = Signal(str)
    progressChanged = Signal(float)
    statusChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self._log = "System Idle."
        self._progress = 0.0
        self._status = "READY"
        self.worker = None

    @Slot(result=str)
    def get_log(self): return self._log

    @Slot(result=float)
    def get_progress(self): return self._progress

    @Slot(result=str)
    def get_status(self): return self._status

    @Slot()
    def start_matrix_computation(self):
        if self.worker and self.worker.isRunning():
            return
        self._status = "PROCESSING"
        self.statusChanged.emit(self._status)
        self.worker = MatrixWorker()
        self.worker.data_received.connect(self.on_data_from_thread)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_data_from_thread(self, log_line, progress_val):
        self._log = log_line
        self._progress = progress_val / 100.0
        self.logChanged.emit(self._log)
        self.progressChanged.emit(self._progress)

    def on_worker_finished(self):
        self._status = "COMPLETED"
        self.statusChanged.emit(self._status)

if __name__ == "__main__":
    QQuickStyle.setStyle("Basic")

    fmt = QSurfaceFormat()
    fmt.setSamples(8)
    QSurfaceFormat.setDefaultFormat(fmt)

    app = QGuiApplication(sys.argv)

    backend = UIBackend()
    engine = QQmlApplicationEngine()

    engine.rootContext().setContextProperty("Backend", backend)

    qml_file = os.path.join(os.path.dirname(__file__), "main.qml")
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
