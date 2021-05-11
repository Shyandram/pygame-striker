import pygame
from res.setting import *
from attitude.game_object import  *
from attitude.Player import  *
from attitude.MyMissile import *
pygame.init()

clock = pygame.time.Clock()

running = True
fps = 60 
movingScale = 600/fps

player = Player(playground=playground,sensitivity = movingScale)

KeyCountX = 0
KeyCountY = 0
Missiles = []
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
                player.to_the_top()
            if event.key == pygame.K_s:
                KeyCountY += 1
                player.to_the_bottom()
            
            if event.key == pygame.K_SPACE:
                # Missile 1 m_x = jet_x/3- missile/2
                m_x = player.x + 9
                m_y = player.y
                Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                # Missile 2 m_x = jet_x*2/3- missile/2
                m_x = player.x + 31
                Missiles.append(MyMissile(playground, (m_x,m_y), movingScale))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or pygame.K_d == event.key:
                if KeyCountX == 0:
                    KeyCountX = 0
                    player.stop_x()
                else:
                    KeyCountX -= 1
                    player.stop_x()
            if event.key == pygame.K_s or pygame.K_w == event.key:
                if KeyCountY == 0:
                    KeyCountY = 0
                    player.stop_y()
                else:
                    KeyCountY -= 1
                    player.stop_y()
        if event.type == pygame.quit:
            running = False
    screen.blit(background,(0,0))
    Missiles = [item for item in Missiles if item.available]
    for m in Missiles:
        m.update()
        screen.blit(m.image, m.xy)

    player.update()
    screen.blit(player.image,player.xy)
    pygame.display.update()
    dt = clock.tick(fps)
pygame.quit()