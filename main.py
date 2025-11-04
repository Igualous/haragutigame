import pygame
import random
# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600)) # width, height

# Background
background = pygame.image.load('media/space.jpg')

# Title and Logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('media/spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('media/battleship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('media/alien_2.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 0.1
enemyY_change = 40


def player(x, y):
    screen.blit(playerImg, (x, y)) # draw player

def enemy(x, y):
    screen.blit(enemyImg, (x, y)) # draw enemy

# Game Loop
running = True
while running:
    # Render background
    screen.fill((10, 0, 10))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # Check Quit
        if event.type == pygame.QUIT:
            running = False
    
        # Check Keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left arrow is pressed")
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                print("Right arrow is pressed")
                playerX_change = 0.3
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Key has being released")
                playerX_change = 0
    
    # Player Movements
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= (800 - 64):
        playerX = (800 - 64)

    
    # Enemy Movements
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change
    elif enemyX >= (800 - 64):
        enemyX_change = -0.3
        enemyY += enemyY_change

    # Render Enemy and Player
    enemy(enemyX, enemyY)
    player(playerX, playerY)

    # update display
    pygame.display.update()