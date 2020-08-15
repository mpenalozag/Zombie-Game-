# ACA SE CREARA LA CLASE QUE MANEJARA EL BACK END DEL JUGADOR
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from parametros import jugador_caminando, jugador_quieto
from parametros import limites


class Jugador(QObject):

    senal_cambia_sprite = pyqtSignal(dict)
    senal_sprite_quieto = pyqtSignal(dict)
    senal_jugador_moviendose = pyqtSignal()
    senal_realizar_disparo = pyqtSignal(str)

    def __init__(self, vida, nivel):
        super().__init__()
        self.nivel = nivel
        self.vida = vida
        self.velocidad = 18
        self.contador_movimiento = 1
        self.ultima_direccion = 'derecha'
        self.timer_quieto = QTimer()
        self.contador_quieto = 1
        self.timer_quieto.setInterval(200)
        self.timer_quieto.timeout.connect(self.animacion_jugador_quieto)
        self.jugador_quieto()

    def moverse(self, string):
        self.timer_quieto.stop()
        self.senal_jugador_moviendose.emit()
        datos = string.split(',')
        direccion = datos[0]
        posicion_x = datos[1]
        posicion_y = datos[2]
        info = dict()
        if direccion == "izquierda":
            info['velocidad'] = -self.velocidad
            info['movimiento'] = jugador_caminando['izquierda'][self.contador_movimiento]
            info['direccion'] = 'izquierda'
            info = self.colisiones_limites_mapa(posicion_x, posicion_y, info)
            self.contador_movimiento += 1
            self.senal_cambia_sprite.emit(info)
            self.ultima_direccion = 'izquierda'
        if direccion == "derecha":
            info['velocidad'] = self.velocidad
            info['movimiento'] = jugador_caminando['derecha'][self.contador_movimiento]
            info['direccion'] = 'derecha'
            info = self.colisiones_limites_mapa(posicion_x, posicion_y, info)
            self.contador_movimiento += 1
            self.senal_cambia_sprite.emit(info)
            self.ultima_direccion = 'derecha'
        if direccion == "arriba":
            if self.ultima_direccion == 'derecha':
                info['velocidad'] = -self.velocidad
                info['movimiento'] = jugador_caminando['derecha'][self.contador_movimiento]
                info['direccion'] = 'arriba'
                info = self.colisiones_limites_mapa(
                    posicion_x, posicion_y, info)
                self.contador_movimiento += 1
                self.senal_cambia_sprite.emit(info)
                self.ultima_direccion = 'derecha'
            if self.ultima_direccion == 'izquierda':
                info['velocidad'] = -self.velocidad
                info['movimiento'] = jugador_caminando['izquierda'][self.contador_movimiento]
                info['direccion'] = 'arriba'
                info = self.colisiones_limites_mapa(
                    posicion_x, posicion_y, info)
                self.contador_movimiento += 1
                self.senal_cambia_sprite.emit(info)
                self.ultima_direccion = 'izquierda'
        if direccion == "abajo":
            if self.ultima_direccion == 'derecha':
                info['velocidad'] = self.velocidad
                info['movimiento'] = jugador_caminando['derecha'][self.contador_movimiento]
                info['direccion'] = 'abajo'
                info = self.colisiones_limites_mapa(
                    posicion_x, posicion_y, info)
                self.contador_movimiento += 1
                self.senal_cambia_sprite.emit(info)
                self.ultima_direccion = 'derecha'
            if self.ultima_direccion == 'izquierda':
                info['velocidad'] = self.velocidad
                info['movimiento'] = jugador_caminando['izquierda'][self.contador_movimiento]
                info['direccion'] = 'abajo'
                info = self.colisiones_limites_mapa(
                    posicion_x, posicion_y, info)
                self.contador_movimiento += 1
                self.senal_cambia_sprite.emit(info)
                self.ultima_direccion = 'izquierda'
        if self.contador_movimiento == 5:
            self.contador_movimiento = 1

    def jugador_quieto(self):
        self.timer_quieto.start()

    def animacion_jugador_quieto(self):
        info = dict()
        info['direccion'] = 'quieto'
        info['movimiento'] = jugador_quieto[self.ultima_direccion][self.contador_quieto]
        self.contador_quieto += 1
        if self.contador_quieto == 3:
            self.contador_quieto = 1
        self.senal_sprite_quieto.emit(info)

    def disparar(self):
        self.senal_realizar_disparo.emit(self.ultima_direccion)

    def colisiones_limites_mapa(self, posicion_x, posicion_y, info):
        # Info es el diccionario que se enviara al front end para hacer el movimiento de la imagen
        if int(posicion_x) + info['velocidad'] < limites['izquierda'] and info['direccion'] == 'izquierda':
            info['velocidad'] = 0
        if int(posicion_x) + info['velocidad'] > limites['derecha'] and info['direccion'] == 'derecha':
            info['velocidad'] = 0
        if int(posicion_y) + info['velocidad'] < limites['superior'] and info['direccion'] == 'arriba':
            info['velocidad'] = 0
        if int(posicion_y) + info['velocidad'] > limites['inferior'] and info['direccion'] == 'abajo':
            info['velocidad'] = 0
        return info
