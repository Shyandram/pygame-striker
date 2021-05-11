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

KeyCountX = 0
KeyCountY = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                KeyCountX += 1
                player.to_the_left()
            if event.key == pygame.K_d:
                KeyCountX -= 1
                player.to_the_right()
            if event.key == pygame.K_w:
                KeyCountY -= 1
                player.to_the_bottom()
            if event.key == pygame.K_s:
                KeyCountY += 1
                player.to_the_top()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or pygame.K_d == event.key:
                if KeyCountX == 1:
                    KeyCountX = 0
                    player.stop_x()
                else:
                    KeyCountX -= 1
            if event.key == pygame.K_s or pygame.K_w == event.key:
                if KeyCountY == 1:
                    KeyCountY = 0
                    player.stop_y()
                else:
                    KeyCountY -= 1
                
        if event.type == pygame.quit:
            running = False
    screen.blit(background,(0,0))
    
    player.update()
    screen.blit(player.image,player.xy)
    pygame.display.update()
    dt = clock.tick(fps)
pygame.quit()