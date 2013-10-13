from assets import Player, Camera

import pygame

def camera_update(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	return Rect(-l + 400, -t + 300, w, h)

WATER_TOP = 500
CENTAUR_PLATFORM = 100


class Water(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([800, 100])
		self.image.fill((0, 0, 255))
		self.rect = self.image.get_rect()
		self.rect.topleft = 0, WATER_TOP

class Goal(pygame.sprite.Sprite):
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.topleft = 750, 550

class Centaur(pygame.sprite.Sprite):
	def __init__(self, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/enemy.png')
		self.rect = self.image.get_rect()
		self.rect.topleft = 0, y
		self.y = y

	def update(self, player):
		self.rect.topleft = (player.rect.topleft[0], self.y)

class SinkingPlayer(Player):
	air_speed = 5
	water_speed = 2
	isFalling = 1

	def move(self, event):
		if (event.type == pygame.KEYDOWN):
			if event.key == pygame.K_UP:
					self.isJumping = 1
			if event.key == pygame.K_RIGHT:
					self.movingRight = 1
			if event.key == pygame.K_LEFT:
					self.movingLeft = 1

		if (event.type == pygame.KEYUP):
			if event.key == pygame.K_RIGHT:
				self.movingRight = 0
			if event.key == pygame.K_LEFT:
				self.movingLeft = 0

	def update(self, in_water):
		movement = [0, 0]
		if (self.movingLeft == 1):
			movement[0] = -2
		if (self.movingRight == 1):
			movement[0] = 2
		if (self.isJumping == 1):
			movement[1] = -20
			self.isJumping = 0

		elif (self.isFalling == 1):
			movement[1] = self.water_speed if in_water else self.air_speed

		self.rect = self.rect.move(movement)

def main():
	# game objects
	things = pygame.sprite.OrderedUpdates()
	player = SinkingPlayer(0, WATER_TOP)
	centaur = Centaur(CENTAUR_PLATFORM)
	goal = Goal("images/goal.png")
	camera = Camera(camera_update, 400, 600)
	water = Water()
	
	things.add(water)
	things.add(centaur)
	things.add(player)
	things.add(goal)
	
	background = pygame.image.load("images/rockyBackground.png")
	backgroundRect = background.get_rect()

	# screen
	size = width, height = 800, 600
	screen = pygame.display.set_mode(size)

	pygame.init()

	timer = pygame.time.Clock()

	while 1:
		timer.tick(40)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			player.move(event)

		screen.fill((0, 0, 0))
		screen.blit(background, backgroundRect)
		
		things.draw(screen)
		player.update(player.rect.colliderect(water.rect))
		centaur.update(player)
		
		if (player.rect.top > 600 or player.rect.left < 0 or player.rect.top < 488 or player.rect.right > 800):
			print "You lose"
			return
		
		if (player.rect.colliderect(goal.rect)):
			print "You win"
			return


		pygame.display.flip()

if __name__ == '__main__': main()
