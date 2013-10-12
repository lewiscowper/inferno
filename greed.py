import sys, pygame
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

def main():
    platformImage = "images/platform.png"
    size = width, height = 800, 600
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    player = Player("images/player.png")

    platformList = []
    for i in range (0, 100):
        platform = Platform(platformImage, i*50, 600)
        platformList.append(platform)

    platformSprites = pygame.sprite.RenderPlain(platformList)

    #goalImage = pygame.image.load("images/goal.png")
    #goalRect = goalImage.get_rect()
    #goalRect.topleft = 700, 500

    clock = pygame.time.Clock()

    camera = Camera(camera_update, 300, 600)

    while 1:
        screen.fill(black)
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

        player.update()
        camera.update(player)
        platformList.extend([player])
        for e in platformList:
            if s:
                screen.blit(s, camera.scroll(e))

        # platformSprites.draw(screen)        
        # screen.blit(player.image, camera.state.topleft + player.rect.topleft)
        #screen.blit(goalImage, goalRect)

        pygame.display.flip()

        if (player.rect.bottom > 600):
            print "Game over"
            return
        
        if (player.rect.colliderect(goalRect)):
            print "You win!"
            return

if __name__ == '__main__': main()
