import sys, pygame, assets, parallax
from pygame import Rect
from assets import Player
from assets import Platform
from assets import Camera
from pygame.locals import *


pygame.init()

HALF_WIDTH = 400
HALF_HEIGHT = 300

def camera_update(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

class Goal(pygame.sprite.Sprite):
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.topleft = 500,40

size = width, height = 800, 600
screen = pygame.display.set_mode((size), pygame.DOUBLEBUF)

bg = parallax.ParallaxSurface([800,600])
bg.add('images/rockyBackground.png', 2)
bgSpeed = 0
t_ref = 0

def main():	
	black = 0, 0, 0
	
	bgSpeed = 0

	player = Player(15, 580)

	platformList = []
	for i in range (0, 10):
		platform = Platform(i*50, 600 - (i*50))
		platformList.append(platform)

	platformSprites = pygame.sprite.RenderPlain(platformList)
	goal = Goal("images/goal.png")

	clock = pygame.time.Clock()

	camera = Camera(camera_update, 300, 600)

	platformList.extend([player, goal])

	while 1:
		screen.fill(black)
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_RIGHT:
				bgSpeed = 10
				player.move(event)
			elif event.type == KEYUP and event.key == K_RIGHT:
				bgSpeed = 0
				player.move(event)
			elif event.type == KEYDOWN and event.key == K_LEFT:
				bgSpeed = -10
				player.move(event)
			elif event.type == KEYUP and event.key == K_LEFT:
				bgSpeed = 0
				player.move(event)
			elif event.type == KEYDOWN and event.key == K_UP:
				player.move(event)
			
		bg.scroll(bgSpeed)
		t = pygame.time.get_ticks()
		if (t - t_ref) > 60:
			bg.draw(screen)

		if (not pygame.sprite.spritecollide(player, platformSprites, False)):
			player.isFalling = 1
		else:
			player.isFalling = 0

		player.update()
		camera.update(player)
		for e in platformList:
			try:
				s = e.image
			except:
				pass
			if s:
				screen.blit(s, camera.scroll(e))
 
		pygame.display.flip()
		
		if (player.rect.left < -10 and player.rect.top > 600):
				print "You win"
				return
			
		if (player.rect.colliderect(goal.rect)):
			player.rect.topleft = 100,100
			print(bgSpeed)
			bgSpeed = 0
			main()
			return
	
		if (player.rect.left >= 0 and player.rect.top > 650):
			player.rect.topleft = 100,100
			print(bgSpeed)
			bgSpeed = 0
			main()
			return

if __name__ == '__main__': main()
