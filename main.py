import pygame
pygame.init()

screenHigh = 760
screenWidth = 1000
playground = [screenWidth,screenHigh]
screen = pygame.display.set_mode((screenWidth,screenHigh))

running = True
fps = 60 
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False
    pygame.display.update()
    dt = clock.tick(fps)
pygame.quit()