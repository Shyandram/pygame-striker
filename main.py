import pygame
from res.setting import screen,background
pygame.init()

running = True
fps = 60 
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False
    screen.blit(background,(0,0))
    pygame.display.update()
    dt = clock.tick(fps)
pygame.quit()