from PyQt5.QtCore import QThread, pyqtSignal
from parametros import limites

import time
import random


class Ronda(QThread):

    senal_enviar_zombies = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.ronda = 1
        self.velocidad = 10
        self.zombies = 2
        self.spawn_speed = 3000/self.ronda  # Milisegundos
        self.activa = False

    def zombies_por_ronda(self):
        return (self.ronda*self.zombies)

    def get_position_zombie(self):
        direccion = random.choice(['derecha', 'izquierda'])
        posicion_y = random.randint(limites['superior'], limites['inferior'])
        info = dict()
        info['direccion'] = direccion
        info['posicion_y'] = posicion_y
        return info

    def generar_zombie(self):
        info = self.get_position_zombie()
        self.senal_enviar_zombies.emit(info)

    def run(self):
        for i in range(self.zombies_por_ronda()):
            time.sleep(self.spawn_speed/1000)
            self.generar_zombie()
        self.ronda_terminada()
        time.sleep(5)
        self.run()

    def ronda_terminada(self):
        self.ronda += 1
