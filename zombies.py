from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal

from parametros import zombie_caminando, limites

import time
import os


class Zombie(QLabel):
    def __init__(self, parent, posicion_y, direccion, id_zombie):
        super().__init__(parent)
        self.direccion = direccion
        self.id_zombie = id_zombie
        self.vida = 20
        self.sprites = None
        self.contador_caminar = 1
        self.set_img()
        self.img_zombie = None
        self.assign_position(posicion_y)

    def set_img(self):
        if self.direccion == 'derecha':
            self.sprites = zombie_caminando['derecha']
        if self.direccion == 'izquierda':
            self.sprites = zombie_caminando['izquierda']
        self.img_zombie = QPixmap(os.path.join(
            *self.sprites[self.contador_caminar]))
        self.setPixmap(self.img_zombie)
        self.resize(51, 81)
        self.setScaledContents(True)

    def assign_position(self, posicion_y):
        if self.direccion == 'derecha':
            self.move(limites['izquierda'], posicion_y)
        if self.direccion == 'izquierda':
            self.move(limites['derecha'], posicion_y)

    def cambiar_sprite(self):
        self.contador_caminar += 1
        if self.contador_caminar == 5:
            self.contador_caminar = 1
        self.img_zombie = QPixmap(os.path.join(
            *self.sprites[self.contador_caminar]))
        self.setPixmap(self.img_zombie)
        self.update()


class ThreadZombie(QThread):

    senal_mover_zombie = pyqtSignal(dict)
    senal_eliminar_zombie = pyqtSignal(float)
    senal_cambiar_sprite_zombie = pyqtSignal()

    def __init__(self, id_zombie, direccion):
        super().__init__()
        self.direccion = direccion
        self.id_zombie = id_zombie
        self.velocidad = 40
        self.activo = True

    def run(self):
        info_move = dict()
        info_move['direccion'] = self.direccion
        info_move['velocidad'] = self.velocidad
        if info_move['direccion'] == 'izquierda':
            info_move['velocidad'] = -self.velocidad
        info_move['id_zombie'] = self.id_zombie
        while self.activo:
            self.senal_mover_zombie.emit(info_move)
            self.senal_cambiar_sprite_zombie.emit()
            time.sleep(0.8)
        self.senal_eliminar_zombie.emit(self.id_zombie)
