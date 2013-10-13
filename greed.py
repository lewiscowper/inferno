import sys, pygame, random, parallax
from pygame import Rect
from assets import Player
from assets import Platform
from assets import Camera
from assets import Wall
from assets import Goal
from pygame.locals import *

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode((size), pygame.DOUBLEBUF)

bg = parallax.ParallaxSurface([800,600])
bg.add('images/rockyBackground.png', 5)
bgSpeed = 0
t_ref = 0

def camera_update(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	return Rect(-l , -t, w, h)

def createPlatforms():
	assetList = []
	
	# add first platform
	previousPlatform = firstPlatform = Platform(0, 300)
	assetList.append(firstPlatform)
	
	for i in range (0, 30):
		heightDifference = random.randint(-30, 30) + previousPlatform.rect.top

		# keep the heights of the platform in a reasonable range
		if (heightDifference > 500):
			heightDifference = 400
		elif (heightDifference < 200):
			heightDifference = 200
			
		platform = Platform(i * 100, heightDifference)
		assetList.append(platform)
		
		#keep the current platform for the next iteration
		previousPlatform = platform
	return assetList

def main():
	black = 28, 19, 02

	bgSpeed = 1.75

	# create assets and add to asset list
	assetList = createPlatforms()
	lastPlatform = assetList[-1] # grab last platform for the goal
	platformSprites = pygame.sprite.RenderPlain(assetList)
	
	goal = Goal(lastPlatform.rect.centerx, lastPlatform.rect.centery - 30)
	assetList.append(goal)
	
	player = Player(100, 250)
	assetList.append(player)
	
	wall = Wall()
	assetList.append(wall)
	
	# Create camera
	camera = Camera(camera_update, 300, 600)
	
	# Create clock
	clock = pygame.time.Clock()

	while 1:
		screen.fill(black)
		
		# tick to lock frame rate
		clock.tick(60)
	
		# handle quit, and parallax scrolling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			player.move(event)

#			elif event.type == KEYDOWN and event.key ==K_RIGHT:
#				bgSpeed = 1.75
#				player.move(event)
#			elif event.type == KEYUP and event.key == K_RIGHT:
#				bgSpeed = 0
#				player.move(event)
#			elif event.type == KEYDOWN and event.key == K_LEFT:
#				bgSpeed = -1.75
#				player.move(event)
#			elif event.type == KEYUP and event.key == K_LEFT:
#				bgSpeed = 0
#				player.move(event)
#			elif event.type == KEYDOWN and event.key == K_UP:
#				player.move(event)
		
		bg.scroll(bgSpeed)
		t = pygame.time.get_ticks()
		if (t - t_ref) > 60:
			bg.draw(screen)

		# do collisions with platform
		if (not pygame.sprite.spritecollide(player, platformSprites, False)):
			player.isFalling = 1
		else:
			player.isFalling = 0
			
		# update all the things
		player.update()
		wall.update()
		camera.update(wall)
		
		# do the redraw
		for e in assetList:
			try:
				s = e.image
			except:
				pass
			if s:
				screen.blit(s, camera.scroll(e))
		
		pygame.display.flip()

		if (player.rect.bottom > 600 or player.rect.colliderect(wall)):
			print "Game over"
			return
		
		if (player.rect.colliderect(goal)):
			print "You win!"
			return

if __name__ == '__main__': main()
