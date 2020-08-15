### IMAGENES ###

# JUGADOR CAMINANDO
jugador_caminando = dict()
jugador_caminando['derecha'] = {1: ('Cenas', 'Player', 'Run(1).png')}
jugador_caminando['derecha'][2] = ('Cenas', 'Player', 'Run(2).png')
jugador_caminando['derecha'][3] = ('Cenas', 'Player', 'Run(3).png')
jugador_caminando['derecha'][4] = ('Cenas', 'Player', 'Run(4).png')

jugador_caminando['izquierda'] = {1: ('Cenas', 'Player', 'Run(1) left.png')}
jugador_caminando['izquierda'][2] = ('Cenas', 'Player', 'Run(2) left.png')
jugador_caminando['izquierda'][3] = ('Cenas', 'Player', 'Run(3) left.png')
jugador_caminando['izquierda'][4] = ('Cenas', 'Player', 'Run(4) left.png')

# JUGADOR QUIETO
jugador_quieto = dict()
jugador_quieto['derecha'] = {1: ('Cenas', 'Player', 'Idle(1).png')}
jugador_quieto['derecha'][2] = ('Cenas', 'Player', 'Idle(2).png')

jugador_quieto['izquierda'] = {1: ('Cenas', 'Player', 'Idle(1) left.png')}
jugador_quieto['izquierda'][2] = ('Cenas', 'Player', 'Idle(2) left.png')

# ZOMBIE
zombie_caminando = dict()
zombie_caminando['derecha'] = {1: ('Cenas', 'Zombie', 'Z_Walk(1).png')}
zombie_caminando['derecha'][2] = ('Cenas', 'Zombie', 'Z_Walk(2).png')
zombie_caminando['derecha'][3] = ('Cenas', 'Zombie', 'Z_Walk(3).png')
zombie_caminando['derecha'][4] = ('Cenas', 'Zombie', 'Z_Walk(4).png')

zombie_caminando['izquierda'] = {1: ('Cenas', 'Zombie', 'Z_Walk(1) left.png')}
zombie_caminando['izquierda'][2] = ('Cenas', 'Zombie', 'Z_Walk(2) left.png')
zombie_caminando['izquierda'][3] = ('Cenas', 'Zombie', 'Z_Walk(3) left.png')
zombie_caminando['izquierda'][4] = ('Cenas', 'Zombie', 'Z_Walk(4) left.png')

zombie_size = (51, 81)


# BALA
bala_derecha = ('Cenas', 'Items', 'Bullet.png')
bala_izquierda = ('Cenas', 'Items', 'Bullet left.png')

bala_size = (13, 47)


### DATOS ###

# LIMITES MAPA
limites = dict()
limites['superior'] = 352
limites['inferior'] = 548
limites['izquierda'] = 0
limites['derecha'] = 1114
