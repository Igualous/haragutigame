import pygame

class Prota(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.image = pygame.image.load('media/prota_frente.png') # sprite

        self.rect = self.image.get_rect(midbottom = (screen_width / 2, screen_height / 2)) # posicao
 
        self.speed = 6 # velocidade

        self.screen_width = screen_width
        
        self.screen_height = screen_height

    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0

    def update(self):
        self.get_user_input()
        self.constrain_movement()