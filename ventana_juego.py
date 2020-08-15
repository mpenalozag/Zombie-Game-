import sys
import os
import random

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal

from bala import ImagenBala, ThreadBala
from zombies import Zombie, ThreadZombie


window_name, base_class = uic.loadUiType('mapa.ui')


class VentanaJuego(window_name, base_class):

    senal_moverse = pyqtSignal(str)
    senal_disparar = pyqtSignal()
    senal_comenzar_ronda = pyqtSignal()
    senal_crear_rect_objeto = pyqtSignal(dict)
    senal_mover_rect = pyqtSignal(dict)
    senal_eliminar_rect = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.zombies = dict()
        self.thread_zombies = dict()
        self.balas = dict()
        self.thread_balas = dict()
        self.boton_comenzar.clicked.connect(self.comenzar_ronda)

    def keyPressEvent(self, event):
        if event.key() == 16777234:  # IZQUIERDA
            self.senal_moverse.emit(f'izquierda,{self.jugador.x()},{self.jugador.y()}')
        if event.key() == 16777236:  # DERECHA
            self.senal_moverse.emit(f'derecha,{self.jugador.x()},{self.jugador.y()}')
        if event.key() == 16777235:  # ARRIBA
            self.senal_moverse.emit(f'arriba,{self.jugador.x()},{self.jugador.y()}')
        if event.key() == 16777237:  # ABAJO
            self.senal_moverse.emit(f'abajo,{self.jugador.x()},{self.jugador.y()}')
        if event.key() == 32:
            self.senal_disparar.emit()

    def mousePressEvent(self, event):
        print(self.jugador.x(), self.jugador.y())

    def cambiar_sprite_jugador(self, info):
        # La ruta viene en una tupla
        sprite_nueva = QPixmap(os.path.join(*info['movimiento']))
        self.jugador.setPixmap(sprite_nueva)

        if info['direccion'] == 'derecha':
            self.jugador.move(self.jugador.x() +
                              info['velocidad'], self.jugador.y())
        if info['direccion'] == 'izquierda':
            self.jugador.move(self.jugador.x() +
                              info['velocidad'], self.jugador.y())
        if info['direccion'] == 'arriba':
            self.jugador.move(self.jugador.x(),
                              self.jugador.y() + info['velocidad'])
        if info['direccion'] == 'abajo':
            self.jugador.move(self.jugador.x(),
                              self.jugador.y() + info['velocidad'])
        self.update()

    def disparar(self, direccion):
        if direccion == 'izquierda':
            bala = ImagenBala(self, self.jugador.x() + 30,
                              self.jugador.y() + 27, 'izquierda')
        if direccion == 'derecha':
            bala = ImagenBala(self, self.jugador.x() + 5,
                              self.jugador.y() + 27, 'derecha')
        info_bala = dict()
        info_bala['x'] = bala.x()
        info_bala['y'] = bala.y()
        info_bala['tipo'] = 'bala'
        self.crear_bala(bala, direccion, info_bala)

    def crear_bala(self, bala, direccion, info_bala):
        id_bala = random.random()
        while id_bala in self.balas:
            id_bala = random.random()
        info_bala['id_objeto'] = id_bala
        self.balas[id_bala] = bala
        thread_bala = ThreadBala(id_bala, direccion)
        thread_bala.senal_dict_bala.connect(self.mover_bala)
        thread_bala.senal_eliminar_bala.connect(self.eliminar_bala)
        self.thread_balas[id_bala] = thread_bala
        self.thread_balas[id_bala].start()
        self.senal_crear_rect_objeto.emit(info_bala)
        bala.show()
        self.update()

    def mover_bala(self, info):
        bala_a_mover = self.balas[info['id_bala']]
        bala_a_mover.move(bala_a_mover.x() +
                          info['velocidad'], bala_a_mover.y())
        info['tipo'] = 'bala'
        info['id_objeto'] = info['id_bala']
        self.senal_mover_rect.emit(info)
        self.check_vida_bala(bala_a_mover, info['id_bala'])

    def check_vida_bala(self, bala, id_bala):
        if bala.x() < 0 or bala.x() > 1172:
            self.thread_balas[id_bala].activa = False

    def comenzar_ronda(self):
        self.boton_comenzar.setEnabled(False)
        self.boton_comenzar.hide()
        self.senal_comenzar_ronda.emit()

    def spawn_zombie(self, info):
        # Info contiene direccion y posicion en y
        info_zombie = dict()
        id_zombie = random.random()
        while id_zombie in self.zombies:
            id_zombie = random.random()
        self.zombies[id_zombie] = Zombie(
            self, info['posicion_y'], info['direccion'], id_zombie)
        info_zombie['x'] = self.zombies[id_zombie].x()
        info_zombie['y'] = self.zombies[id_zombie].y()
        info_zombie['tipo'] = 'zombie'
        info_zombie['id_objeto'] = id_zombie
        thread_zombie = ThreadZombie(id_zombie, info['direccion'])
        thread_zombie.senal_mover_zombie.connect(self.mover_zombie)
        thread_zombie.senal_eliminar_zombie.connect(self.eliminar_zombie)
        thread_zombie.senal_cambiar_sprite_zombie.connect(
            self.zombies[id_zombie].cambiar_sprite)
        self.thread_zombies[id_zombie] = thread_zombie
        self.thread_zombies[id_zombie].start()
        self.senal_crear_rect_objeto.emit(info_zombie)
        self.zombies[id_zombie].show()
        self.update()

    def mover_zombie(self, info):
        # info contiene direccion, velocidad e id_zombie
        zombie = self.zombies[info['id_zombie']]
        # Velocidad ya viene definida segun la direccion, no es necesario cambiarlo. Solo hay que sumarla a x
        zombie.move(zombie.x() + info['velocidad'], zombie.y())
        info['id_objeto'] = info['id_zombie']
        info['tipo'] = 'zombie'
        self.senal_mover_rect.emit(info)

    def eliminar_bala(self, id_bala):
        self.balas[id_bala].hide()
        del self.balas[id_bala]

    def eliminar_zombie(self, id_zombie):
        self.zombies[id_zombie].hide()
        del self.zombies[id_zombie]

    def eliminar_objeto(self, info):
        # info contiene tipo, id_objeto
        id_objeto = info['id_objeto']
        if info['tipo'] == 'zombie':
            self.thread_zombies[id_objeto].activo = False
            del self.thread_zombies[id_objeto]
            self.eliminar_rect(info)
        if info['tipo'] == 'bala':
            if id_objeto in self.thread_balas:
                self.thread_balas[id_objeto].activa = False
                del self.thread_balas[id_objeto]
            self.eliminar_rect(info)

    def eliminar_rect(self, info):
        # info contiene el tipo de objeto y además el id del objeto
        self.senal_eliminar_rect.emit(info)

    def ronda_terminada(self):
        self.boton_comenzar.setEnabled(True)
        self.boton_comenzar.show()


if __name__ == '__main__':
    app = QApplication([])
    game_window = VentanaJuego()
    sys.exit(app.exec_())
