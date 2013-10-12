import sys, pygame, assets
from pygame import Rect
from assets import Player
from assets import Platform
from assets import Camera

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
	    self.rect.topleft = 500,400
def main():
    platformImage = "images/platform.png"
    size = width, height = 800, 600
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    player = Player("images/player.png", 100, 100)

    platformList = []
    for i in range (0, 10):
        platform = Platform(platformImage, i*50, 600 - (i*50))
        platformList.append(platform)

    platformSprites = pygame.sprite.RenderPlain(platformList)
    goal = Goal("images/goal.png")

    clock = pygame.time.Clock()

    camera = Camera(camera_update, 300, 600)

    while 1:
        screen.fill(black)
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            else:
                player.move(event)
        
        if (not pygame.sprite.spritecollide(player, platformSprites, False)):
            player.isFalling = 1
        else:
            player.isFalling = 0

        player.update()
        camera.update(player)
        platformList.extend([player, goal])
        for e in platformList:
            try:
                s = e.image
            except:
                pass
            if s:
                screen.blit(s, camera.scroll(e))
 
        pygame.display.flip()

        if (player.rect.bottom > 610):
            print "You win"
            return
        
        if (player.rect.colliderect(goal.rect)):
            player.rect.topleft = 100,100
	    main()
            return

if __name__ == '__main__': main()
