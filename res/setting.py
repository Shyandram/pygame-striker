from pathlib import Path
import pygame

parent_path = Path(__file__).parents[1]
image_path = parent_path/'res'
icon_path = image_path / 'jet_icon.png'

pygame.init()

screenHigh = 760
screenWidth = 1000
playground = [screenWidth,screenHigh]
screen = pygame.display.set_mode((screenWidth,screenHigh))

pygame.display.set_caption("fake 1942")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
background = pygame.Surface(screen.get_size())
background.fill((50,50,50))
background = background.convert()