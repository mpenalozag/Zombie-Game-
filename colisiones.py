from PyQt5.QtCore import QRect, QObject, pyqtSignal
from parametros import zombie_size, bala_size


class Colisiones(QObject):

	senal_eliminar_objeto = pyqtSignal(dict)

	def __init__(self):
		super().__init__()
		# Cada diccionario tendrá como key el id de cada objeto
		# y el item será el rect
		self.zombies = dict()
		self.balas = dict()

	def mover_rect(self, info):
		tipo = info['tipo']
		id_objeto = info['id_objeto']
		velocidad = info['velocidad']
		if tipo == 'zombie':
			zombie = self.zombies[id_objeto]
			zombie.moveTo(zombie.x() + velocidad, zombie.y())
			self.chequear_colisiones(zombie, 'zombie', id_objeto)
		if tipo == 'bala':
			bala = self.balas[id_objeto]
			bala.moveTo(bala.x() + velocidad, bala.y())
			self.chequear_colisiones(bala, 'bala', id_objeto)

	def crear_rect(self, info):
		# Info es un dict con id_objeto, tipo, pos x, pos y
		tipo = info['tipo']
		pos_x = info['x']
		pos_y = info['y']
		id_objeto = info['id_objeto']
		if tipo == 'zombie':
			rectangulo = PersonalizedRect(id_objeto, tipo, pos_x, pos_y, *zombie_size)
			self.zombies[id_objeto] = rectangulo
		if tipo == 'bala':
			rectangulo = PersonalizedRect(id_objeto, tipo, pos_x, pos_y, *bala_size)
			self.balas[id_objeto] = rectangulo

	def chequear_colisiones(self, rect, tipo, id_objeto):
		# Entra el rect del objeto
		if tipo == 'zombie':
			for key, objeto in self.balas.items():
				if rect.intersects(objeto):
					print('Chocó zombie con bala')
					self.eliminar_objeto(id_objeto, tipo)
					self.eliminar_objeto(objeto.id_objeto, objeto.tipo)
					return
		elif tipo == 'bala':
			for key, objeto in self.zombies.items():
				if rect.intersects(objeto):
					print('Chocó bala con zombie')
					self.eliminar_objeto(id_objeto, tipo)
					self.eliminar_objeto(objeto.id_objeto, objeto.tipo)
					return

	def eliminar_objeto(self, id_objeto, tipo):
		info = dict()
		info['tipo'] = tipo
		info['id_objeto'] = id_objeto
		self.senal_eliminar_objeto.emit(info)

	def eliminar_rect(self, info):
		# info contiene tipo de objeto y el id del objeto
		if info['tipo'] == 'zombie':
			self.zombies[info['id_objeto']].moveTo(5000, 5000)
			del self.zombies[info['id_objeto']]
		if info['tipo'] == 'bala':
			self.balas[info['id_objeto']].moveTo(5000, 5000)
			del self.balas[info['id_objeto']]



class PersonalizedRect(QRect):
	def __init__(self, id_objeto, tipo, *parent):
		super().__init__(*parent)
		self.id_objeto = id_objeto
		self.tipo = tipo
