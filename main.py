import pygame
from res.setting import *
from attitude.game_object import  *
from attitude.Player import  *

pygame.init()

clock = pygame.time.Clock()

running = True
fps = 60 
movingScale = 600/fps

player = Player(playground=playground,sensitivity = movingScale)



while running:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False
    screen.blit(background,(0,0))
    
    player.update()
    screen.blit(player.image,player.xy)
    pygame.display.update()
    dt = clock.tick(fps)
pygame.quit()