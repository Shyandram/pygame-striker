import pygame
from res.setting import *
from attitude.game_object import  *
from attitude.Player import  *
from attitude.MyMissile import *
from attitude.EnemyMissile import *
from attitude.Enemy import *
from attitude.explosion import *
from attitude.heal import *
import time

pygame.init()

clock = pygame.time.Clock()

running = True
fps = 60
movingScale = 600/fps

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()
def message_display(text,x,y,size):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((screenWidth-x),(screenHigh-y))
    screen.blit(TextSurf, TextRect)




player = Player(playground=playground,sensitivity = movingScale)

KeyCountX = 0
KeyCountY = 0

Missiles = []
E_Missiles=[]
Enemies = []
Boom = []
Cure = []

launchMissile = pygame.USEREVENT + 1
createEnemy = pygame.USEREVENT + 2
explosion = pygame.USEREVENT + 3
launchEnemyMissile = pygame.USEREVENT + 4

pygame.time.set_timer(createEnemy, 1000)
pygame.time.set_timer(launchEnemyMissile, 1000)

stage0 = False
stage1 = False
dead = False
emtime =0
endtime = 0
score = 0

activate_time = time.time()
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
        if event.type == launchEnemyMissile:
            for e in Enemies:
                e_m_x = e.xy[0] + 20
                e_m_y = e.xy[1]
                E_Missiles.append(EnemyMissile(xy=(e_m_x, e_m_y), playground=playground, sensitivity=movingScale))
                e_m_x = e.xy[0] + 80
                E_Missiles.append(EnemyMissile(xy=(e_m_x, e_m_y), playground=playground, sensitivity=movingScale))
        

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
            if event.key == pygame.K_h:
                if score >20:
                    score -= 20
                    player.hp += 20
                    Cure.append(Heal(player.center))
            if event.key == pygame.K_c:
                if score > 50:
                    score -= 40
                    for e in Enemies:
                        score += 1
                        Boom.append(Explosion(e.center))   
                    E_Missiles=[]
                    Enemies = []
                    
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

    for em in E_Missiles:
        em.collision_detect1(player)

    for e in Enemies:
        if e.collided:
            score += 1
            Boom.append(Explosion(e.center))

    
    Missiles = [item for item in Missiles if item.available]
    for m in Missiles:
        m.update()
        screen.blit(m.image, m.xy)
    
    E_Missiles = [item for item in E_Missiles if item.available]
    for em in E_Missiles:
        em.update()
        screen.blit(em.image, em.xy)

    Enemies = [item for item in Enemies if item.available]
    for e in Enemies:
        # emtime += clock.tick_busy_loop(fps*2)
        # if emtime == 100:
        #     pygame.time.set_timer(launchEnemyMissile, 1000)
        # if emtime == 500:
        #     pygame.time.set_timer(launchEnemyMissile, 0)
        #     emtime = 0
        e.update()
        screen.blit(e.image, e.xy)

    player.update()
    screen.blit(player.image,player.xy)

    Boom = [item for item in Boom if item.available]
    for e in Boom:
        e.update()
        screen.blit(e.image, e.xy)

    Cure = [item for item in Cure if item.available]
    for e in Cure:
        e.update()
        screen.blit(e.image, e.xy)
    
    
    if player.hp <= -99:
        if dead == False:
            dead = True
            dead_time = time.time()
        Enemies = []
        Missiles = []
        E_Missiles=[]
        endtime += clock.tick_busy_loop(fps*3)
        Boom.append(Explosion(player.center))
        player.stop_x()
        player.stop_y()
        message_display("Game Over",screenWidth/2,screenHigh/2,50)
        if stage0 == True:
            message_display("stage0 Clear",screenWidth/2,screenHigh/2-30,20)
            
        if stage1 == True:
            message_display("stage1 Clear",screenWidth/2,screenHigh/2-60,20)
            
        message_display("Final Score: " + str(score),screenWidth/2,screenHigh/2-90,30)
        message_display("Survive Time: " + str(int(dead_time - activate_time))+"sec",screenWidth/2,screenHigh/2-120,20)
        player.hp = -99
        if fps*15 < (endtime):
            running = False
        
    else:
        message_display("Score: "+str(score),screenWidth/2,screenHigh-10,20)
        message_display("Hp: "+str(99 + player.hp),100,50,20)
    
    if score > 20:
        if stage0 == False:
            stage0 = True
            score += 20
            pygame.time.set_timer(launchEnemyMissile, 500)
        message_display("Press h for Heal",100,70,20)
    if score > 50:
        message_display("Press c for Destroy all enemy",screenWidth/2,screenHigh-30,20)

    if score > 70:
        if stage1 == False:
            stage1 = True
            score += 50
            pygame.time.set_timer(createEnemy, 1000)
        
    pygame.display.update()
    dt = clock.tick(fps)
pygame.quit()