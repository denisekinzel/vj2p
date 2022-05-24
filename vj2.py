import pygame
import random
from pygame.locals import(
	K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,RLEACCEL)
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.surf = pygame.image.load("papitas.png").convert()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		# la posicion inicial es generada aleatoriamente, al igual que la velocidad
		self.rect = self.surf.get_rect(
			center = (
								random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
								random.randint(0, SCREEN_HEIGHT),
			)
		)
		self.speed = random.randint(5, 10)
	
	# el sprite tendra velocidad
	# cuando traspase el lado izq de la pantalla lo eliminamos
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()
			
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surf = pygame.image.load("profe_Jorge.png").convert()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surf.get_rect()

	def update(self, pressed_keys):
		if pressed_keys[K_UP]:
			self.rect.move_ip(0, -5)
		if pressed_keys[K_DOWN]:
			self.rect.move_ip(0, 5)
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-5, 0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(5, 0)
	
		# mantener al jugador en pantalla
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > SCREEN_WIDTH:
			self.rect.right = SCREEN_WIDTH
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT
class Cloud(pygame.sprite.Sprite):
	def __init__(self):
		super(Cloud, self).__init__()
		self.surf = pygame.image.load("cloud.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		# posicion inicial random
		self.rect = self.surf.get_rect(
			center = (
								random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
								random.randint(0, SCREEN_HEIGHT),
			)
		)

	# igual que los enemigos
	def update(self):
		self.rect.move_ip(-5, 0)
		if self.rect.right < 0:
			self.kill()

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("san_joaquin.jpg").convert()
# evento para crear enemigos cada cierto intervalo de tiempo
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 350)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()
# creamos grupos para tener a los enemigos y todos los sprites
# cloud para las nubes
# enemies es para detectar colisiones y actualizar posiciones
# all_sprites es para renderizar
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
clock = pygame.time.Clock()
running = True
# loop principal del juego
# loop principal del juego
while running:
	# iteramos sobre cada evento en la cola
	for event in pygame.event.get():
		# se presiono una tecla?
		if event.type == KEYDOWN:
			# era la tecla de escape? -> entonces terminamos
			if event.key == K_ESCAPE:
				running = False

		# fue un click al cierre de la ventana? -> entonces terminamos
		elif event.type == QUIT:
			running = False

		# es un evento que agrega enemigos?
		elif event.type == ADDENEMY:
			new_enemy = Enemy()
			enemies.add(new_enemy)
			all_sprites.add(new_enemy)

		# es un evento que agrega nubes?
		elif event.type == ADDCLOUD:
			new_cloud = Cloud()
			clouds.add(new_cloud)
			all_sprites.add(new_cloud)


	# rellena la screen con u color, en este caso blanco
	screen.blit(background_image, [0, 0])

	# dibujamos todos los sprites
	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)
	# vemos si algun enemigo a chocado con el jugador
	if pygame.sprite.spritecollideany(player, enemies):
		# si pasa, removemos al jugador y detenemos el loop del juego
		player.kill()
		running = False

	# actualizamos la interfaz
	pygame.display.flip()

	# tasa de 30 frames por segundo
	clock.tick(30)

	# obtenemos todas las teclas presionadas actualmente
	pressed_keys = pygame.key.get_pressed()

	# actualizamos el sprite del jugador basado en las teclas presionadas
	player.update(pressed_keys)
	
	# obtenemos todas las teclas presionadas actualmente
	pressed_keys = pygame.key.get_pressed()

	# actualizamos el sprite del jugador basado en las teclas presionadas
	player.update(pressed_keys)

	# actualizamos los enemigos
	enemies.update()

	# actualizamos las nubes
	clouds.update()

