import sys, pygame,random
from pygame import Rect
from assets import Player
from assets import Platform
from assets import Camera
from assets import Wall
from assets import Goal

pygame.init()

size = width, height = 800, 600

def camera_update(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	return Rect(-l , -t, w, h)

def createPlatforms():
	assetList = []
	
	#add first platform
	previousPlatform = firstPlatform = Platform(0, 300)
	assetList.append(firstPlatform)
	
	for i in range (0, 30):
		startingPoint = previousPlatform.rect.top
		heightDifference = random.randint(-50,50) + startingPoint
		if (heightDifference < 400):
			heightDifference = 400
		platform = Platform(i * 100, heightDifference)
		assetList.append(platform)
		previousPlatform = platform
	return assetList

def main():
	black = 0, 0, 0
	screen = pygame.display.set_mode(size)

	# create assets and add to asset list
	assetList = createPlatforms()
	platformSprites = pygame.sprite.RenderPlain(assetList)
	lastPlatform = assetList[-1]
	
	goal = Goal(lastPlatform.rect.centerx, lastPlatform.rect.centery-30)
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
	
		# handle quit
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			else:
				player.move(event)
		
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
