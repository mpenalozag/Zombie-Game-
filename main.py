import sys

from ventana_juego import VentanaJuego
from jugador import Jugador
from PyQt5.QtWidgets import QApplication
from timer import TimerJugador
from ronda import Ronda
from colisiones import Colisiones

# Creamos la app
app = QApplication([])

#Instanciamos los elementos a utilizar#

ventana_juego = VentanaJuego()
player = Jugador(100, 1)
timer_player = TimerJugador()
ronda = Ronda()
colisiones = Colisiones()

# Conectamos señales
ventana_juego.senal_moverse.connect(player.moverse)
player.senal_cambia_sprite.connect(ventana_juego.cambiar_sprite_jugador)
player.senal_jugador_moviendose.connect(timer_player.comenzar)
timer_player.senal_jugador_quieto.connect(player.jugador_quieto)
player.senal_sprite_quieto.connect(ventana_juego.cambiar_sprite_jugador)
ventana_juego.senal_disparar.connect(player.disparar)
player.senal_realizar_disparo.connect(ventana_juego.disparar)
ronda.senal_enviar_zombies.connect(ventana_juego.spawn_zombie)
ventana_juego.senal_comenzar_ronda.connect(ronda.start)
ventana_juego.senal_crear_rect_objeto.connect(colisiones.crear_rect)
ventana_juego.senal_mover_rect.connect(colisiones.mover_rect)
colisiones.senal_eliminar_objeto.connect(ventana_juego.eliminar_objeto)
ventana_juego.senal_eliminar_rect.connect(colisiones.eliminar_rect)


# Creamos loop de la app
sys.exit(app.exec_())
