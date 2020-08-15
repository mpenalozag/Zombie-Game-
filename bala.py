import os
import time
from PyQt5.QtMultimedia import QSound

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from parametros import bala_derecha, bala_izquierda


class ImagenBala(QLabel):
    def __init__(self, parent, pos_x, pos_y, direccion):
        super().__init__(parent)
        self.direccion = direccion
        self.assign_pixmap(pos_x, pos_y)
        self.update()

    def assign_pixmap(self, pos_x, pos_y):
        if self.direccion == 'derecha':
            img_bala = QPixmap(os.path.join(*bala_derecha))
            self.setPixmap(img_bala)
            self.move(pos_x, pos_y)
        if self.direccion == 'izquierda':
            img_bala = QPixmap(os.path.join(*bala_izquierda))
            self.setPixmap(img_bala)
            self.move(pos_x, pos_y)


class ThreadBala(QThread):

    senal_mover_bala = pyqtSignal(dict)
    senal_dict_bala = pyqtSignal(dict)
    senal_eliminar_bala = pyqtSignal(float)

    def __init__(self, num_bala, direccion):
        super().__init__()
        self.direccion = direccion
        self.velocidad = 50
        self.id_bala = num_bala
        self.activa = True
        self.sonido_bala = QSound('disparo.wav')

    def run(self):
        self.sonido_bala.play()
        info_move = dict()
        info_move['velocidad'] = self.velocidad
        info_move['id_bala'] = self.id_bala
        info_move['direccion'] = self.direccion
        if info_move['direccion'] == 'izquierda':
            info_move['velocidad'] = -self.velocidad
        while self.activa:
            self.senal_dict_bala.emit(info_move)
            time.sleep(0.1)
        self.senal_eliminar_bala.emit(self.id_bala)

    def move_bullet(self):
        info = dict()
        info['velocidad'] = self.velocidad
        self.senal_mover_bala.emit()
