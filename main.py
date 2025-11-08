import sys
import pygame
from Robot import Robot

pygame.init()

COR = (4, 4, 53)

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Invasores Galácticos")

clock = pygame.time.Clock()

robot_group = pygame.sprite.GroupSingle(Robot(SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

while running: 
    # Checar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Desenhar
    screen.fill(COR)

    robot_group.update()

    robot_group.draw(screen)

    pygame.display.update()
    clock.tick(60) # Limita a 60 FPS