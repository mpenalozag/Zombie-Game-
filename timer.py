from PyQt5.QtCore import QTimer, QObject, pyqtSignal


class TimerJugador(QObject):

    senal_jugador_quieto = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.jugador_quieto)

    def comenzar(self):
        self.timer.start()

    def jugador_quieto(self):
        self.senal_jugador_quieto.emit()
        self.timer.stop()
