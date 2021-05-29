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
st_running = True
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
E_Missiles =[]
Ex_Missiles = []
Enemies = []
Boom = []
Cure = []

launchMissile = pygame.USEREVENT + 1
createEnemy = pygame.USEREVENT + 2
explosion = pygame.USEREVENT + 3
launchEnemyMissile = pygame.USEREVENT + 4
launchExtraMissile = pygame.USEREVENT + 5

pygame.time.set_timer(createEnemy, 1000)
pygame.time.set_timer(launchEnemyMissile, 1000)

Invincible_str_time=0
Invincible_hp=1
missileup = 0
creater_mode = False
change_missile = False
stage1 = False
stage2 = False
stage3 = False
dead = False
emtime = 0
endtime = 0
score = 0

# add a startup screen
while st_running:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            st_running = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                creater_mode = True
            st_running = False
    message_display("Striker1942",screenWidth/2,screenHigh/2,50)
    message_display("Press a bottom to start",screenWidth/2,screenHigh/2-50,30)
    pygame.display.update()
    dt = clock.tick(fps)

# Main Game
activate_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == launchMissile:
            m_x = player.xy[0] + 8
            m_y = player.xy[1]
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
            m_x = player.xy[0] + 35
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
        if event.type == launchExtraMissile:
            if missileup >0:
                m_x = player.xy[0]
                m_y = player.xy[1]
                Ex_Missiles.append(MyExtraMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                missileup -= 1
                print(missileup)
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
                if change_missile != True:
                    m_x = player.x + 8
                    m_y = player.y
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                    # Missile 2 m_x = jet_x*2/3- missile/2
                    m_x = player.x + 35
                    Missiles.append(MyMissile(playground, (m_x,m_y), movingScale))
                    pygame.time.set_timer(launchMissile, 300)  # 之後，每400 ms發射一組
                else:
                    if missileup >0:
                        m_x = player.xy[0]
                        m_y = player.xy[1]
                        Missiles.append(MyExtraMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                        missileup -= 1
                        pygame.time.set_timer(launchExtraMissile, 300)
            if event.key == pygame.K_m:
                if change_missile:
                    change_missile = False
                else:
                    change_missile = True

            if event.key == pygame.K_h:
                if score >20:
                    score -= 15
                    player.hp += 10
                    Cure.append(Heal(player.center))
                    print("Heal")
            if event.key == pygame.K_k:
                if score > 50:
                    score -= 20
                    for e in Enemies:
                        score += 1
                        Boom.append(Explosion(e.center))   
                    E_Missiles=[]
                    Enemies = []
                    print("Clear all")
            if event.key == pygame.K_l:
                if score > 50 and Invincible_str_time == 0:
                    score -= 25
                    Invincible_str_time = time.time()
                    Invincible_hp = player.hp
                    print("Invincible is on")
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                if KeyCountX == 1:
                    KeyCountX = 0
                    player.stop_x()
                else:
                    KeyCountX -= 1
            if event.key == pygame.K_s or event.key == pygame.K_w:
                if KeyCountY == 1:
                    KeyCountY = 0
                    player.stop_y()
                else:
                    KeyCountY -= 1

            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(launchMissile, 0)  # 停止發射
                pygame.time.set_timer(launchExtraMissile, 0)
    screen.blit(background,(0,0))
    player.collision_detect(Enemies)
    for m in Missiles:
        m.collision_detect(Enemies)

    for em in E_Missiles:
        em.collision_detect1(player)

    for m in Ex_Missiles:
        m.collision_detect(Enemies)

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

    Ex_Missiles = [item for item in Ex_Missiles if item.available]
    for m in Ex_Missiles:
        m.update()
        screen.blit(m.image, m.xy)

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
    
    
    if Invincible_str_time != 0:
        if Invincible_str_time+5 < time.time():
            Invincible_str_time = 0
            print("Invincible is off")
        else:
            player.hp =Invincible_hp
        

    if player.hp <= -99:
        if dead == False:
            dead = True
            dead_time = time.time()
            endtime = dead_time+ 5
        Enemies = []
        Missiles = []
        E_Missiles=[]
        Ex_Missiles = []
        Boom.append(Explosion(player.center))
        player.stop_x()
        player.stop_y()
        message_display("Game Over",screenWidth/2,screenHigh/2,50)
        if stage1 == True:
            message_display("stage0 Clear",screenWidth/2,screenHigh/2-30,20)
            
        if stage2 == True:
            message_display("stage1 Clear",screenWidth/2,screenHigh/2-60,20)
        if stage3 == True:
            message_display("stage2 Clear",screenWidth/2,screenHigh/2-90,20)
            
        message_display("Score: " + str(score),screenWidth/2,screenHigh/2-120,20)
        message_display("Survive Time: " + str(int(dead_time - activate_time))+" sec",screenWidth/2,screenHigh/2-150,20)
        message_display("Final Score(Score + 0.4*Survive Time): " + str(int(score + 0.4*int(dead_time - activate_time))),screenWidth/2,screenHigh/2-170,20)
        player.hp = -99
        if (time.time() ) > (endtime):
            running = False
        
    else:
        message_display("Score: "+str(score),screenWidth/2,screenHigh-10,20)
        message_display("Hp: "+str(99 + player.hp),100,50,20)
        message_display("Ex-Missile:"+str(missileup),110,70,20)
        if change_missile:
            message_display("Missile: Ultra!",screenWidth/2,screenHigh-30,20)
        else:
            message_display("Missile: Normal",screenWidth/2,screenHigh-30,20)

        if score > 20:
            message_display("Press h for Heal",100,screenHigh-50,20)
        if score > 50:
            message_display("Press k for Destroy all enemy",150,screenHigh-70,20)
            message_display("Press l for Invincible",120,screenHigh-90,20)
    if score > 20:
        if stage1 == False:
            stage1 = True
            score += 20
            missileup += 10
            # pygame.time.set_timer(launchEnemyMissile,0)
            # pygame.time.set_timer(createEnemy, 0)
            pygame.time.set_timer(launchEnemyMissile, 900)
            pygame.time.set_timer(createEnemy, 900)
    if score > 100:
        if stage2 == False:
            stage2 = True
            score += 50
            missileup += 50
            # pygame.time.set_timer(launchEnemyMissile,0)
            # pygame.time.set_timer(createEnemy, 0)
            pygame.time.set_timer(launchEnemyMissile, 800)
            pygame.time.set_timer(createEnemy, 800)
    if score > 200:
        if stage3 == False:
            stage3 = True
            score += 100
            missileup += 150
            # pygame.time.set_timer(launchEnemyMissile,0)
            # pygame.time.set_timer(createEnemy, 0)
            pygame.time.set_timer(launchEnemyMissile, 700)
            pygame.time.set_timer(createEnemy, 700)
    if creater_mode:
        message_display("creater_mode",screenWidth/2,screenHigh/2,50)
        player.hp = Invincible_hp
        score = 500
        missileup = 5000

    pygame.display.update()
    dt = clock.tick(fps)
pygame.quit()