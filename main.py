import pygame
from res.setting import *
from attitude.game_object import  *
from attitude.Player import  *
from attitude.MyMissile import *
from attitude.Enemy import *
from attitude.explosion import *
import time

pygame.init()

clock = pygame.time.Clock()

running = True
fps = 60 
movingScale = 600/fps

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((screenWidth-100),(screenHigh-100))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()


player = Player(playground=playground,sensitivity = movingScale)

KeyCountX = 0
KeyCountY = 0

Missiles = []
Enemies = []
Boom = []

launchMissile = pygame.USEREVENT + 1
createEnemy = pygame.USEREVENT + 2
explosion = pygame.USEREVENT + 3

pygame.time.set_timer(createEnemy, 1000)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == launchMissile:
            m_x = player.xy[0] + 9
            m_y = player.xy[1]
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
            m_x = player.xy[0] + 31
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
        if event.type == createEnemy:
            Enemies.append(enemy(playground=playground, sensitivity=movingScale))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                KeyCountX += 1
                player.to_the_left()
            if event.key == pygame.K_d:
                KeyCountX += 1
                player.to_the_right()
            if event.key == pygame.K_w:
                KeyCountY += 1
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
                pygame.time.set_timer(launchMissile, 400)  # 之後，每400 ms發射一組

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
            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(launchMissile, 0)  # 停止發射     
        
    screen.blit(background,(0,0))
    player.collision_detect(Enemies)
    for m in Missiles:
        m.collision_detect(Enemies)

    for e in Enemies:
        if e.collided:
            Boom.append(Explosion(e.center))

    
    Missiles = [item for item in Missiles if item.available]
    for m in Missiles:
        m.update()
        screen.blit(m.image, m.xy)

    Enemies = [item for item in Enemies if item.available]
    for e in Enemies:
        e.update()
        screen.blit(e.image, e.xy)

    player.update()
    screen.blit(player.image,player.xy)

    Boom = [item for item in Boom if item.available]
    for e in Boom:
        e.update()
        screen.blit(e.image, e.xy)
    
    pygame.display.update()
    
    if player.hp == -99:
        Boom.append(Explosion(player.center))
        time.sleep(3)
        running = False

    message_display("Hp: "+str(99 + player.hp))
    pygame.display.update()
    dt = clock.tick(fps)
pygame.quit()