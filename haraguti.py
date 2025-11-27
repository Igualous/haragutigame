import pygame
import sys
import os

# game variables
GAME_WIDTH = 768
GAME_HEIGHT = 768

PLAYER_X = GAME_WIDTH / 2
PLAYER_Y = GAME_HEIGHT / 2
PLAYER_WIDTH = 42
PLAYER_HEIGHT = 80
PLAYER_SHOOT_WIDTH = 62
PLAYER_SHOOT_HEIGHT = PLAYER_HEIGHT

PLAYER_VELOCITY = 5
FRICTION = 0.7

PLAYER_BULLET_WIDTH = 16
PLAYER_BULLET_HEIGHT = 12
PLAYER_BULLET_VELOCITY = 8

HEALTH_WIDTH = 64
HEALTH_HEIGHT = 4

# plant variables
PLANT_X = GAME_WIDTH / 2 - PLAYER_WIDTH / 2
PLANT_Y = GAME_HEIGHT / 2 - PLAYER_HEIGHT / 2
PLANT_WIDTH = 64
PLANT_HEIGHT = 64

# lake variables
LAKE_WIDTH = 256
LAKE_HEIGHT = 128
LAKE_X = GAME_WIDTH * 2/3 - LAKE_WIDTH / 2
LAKE_Y = - LAKE_HEIGHT / 3

# bucket variables
BUCKET_WIDTH = 32
BUCKET_HEIGHT = BUCKET_WIDTH
BUCKET_X = LAKE_X - BUCKET_WIDTH - 10
BUCKET_Y = LAKE_Y + LAKE_HEIGHT - BUCKET_HEIGHT - 10

# enemy variables
NOIA_WIDTH = 64
NOIA_HEIGHT = 96
NOIA_VELOCITY = 0.51

# images
def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join("midia", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

background_image = load_image("background-dirt.png", (GAME_WIDTH, GAME_HEIGHT))
player_image = load_image("zinho.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image("zinho-left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_right = load_image("zinho-right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_back = load_image("zinho-back.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_shoot_left = load_image("zinho-left-shoot.png", (PLAYER_SHOOT_WIDTH, PLAYER_SHOOT_HEIGHT))
player_image_shoot_right = load_image("zinho-right-shoot.png", (PLAYER_SHOOT_WIDTH, PLAYER_SHOOT_HEIGHT))
player_image_shoot_back = load_image("zinho-back-shoot.png", (PLAYER_WIDTH,PLAYER_HEIGHT))
player_shoot_image = load_image("zinho-down-shoot.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
plant_image1 = load_image("planta-01.png", (PLANT_WIDTH, PLANT_HEIGHT))
plant_image2 = load_image("planta-02.png", (PLANT_WIDTH, PLANT_HEIGHT))
lake_image_empty = load_image("lake-empty.png", (LAKE_WIDTH, LAKE_HEIGHT))
lake_image_full = load_image("lake-full.png", (LAKE_WIDTH, LAKE_HEIGHT))
bucket_image_empty = load_image("bucket-empty.png", (BUCKET_WIDTH, BUCKET_HEIGHT))
bucket_image_full = load_image("bucket-full.png", (BUCKET_WIDTH, BUCKET_HEIGHT))
noia_image = load_image("roger.png", (NOIA_WIDTH, NOIA_HEIGHT))
noia_image_left = load_image("roger-left.png", (NOIA_WIDTH, NOIA_HEIGHT))
noia_image_right = load_image("roger-right.png", (NOIA_WIDTH, NOIA_HEIGHT))
noia_image_back = load_image("roger-back.png", (NOIA_WIDTH, NOIA_HEIGHT))
noia_image_dead = load_image("roger-dead.png", (NOIA_WIDTH, NOIA_HEIGHT))
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("A Última Semente")
clock = pygame.time.Clock()

INVINCIBLE_END = pygame.USEREVENT + 0
SHOOTING_END = pygame.USEREVENT + 1
LAKE_RECHARGE = pygame.USEREVENT + 2
class Player(pygame.Rect):
    def __init__(self):
        super().__init__(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "down"
        self.invincible = False
        self.max_health = 100
        self.health = self.max_health
        self.shooting = False
        self.bullets = []
        self.with_bucket = True

    def update_image(self):
        if self.shooting == True:
            if self.direction == "left":
                self.image = player_image_shoot_left
            elif self.direction == "right":
                self.image = player_image_shoot_right
            elif self.direction == "up":
                self.image = player_image_shoot_back
            else:
                self.image = player_shoot_image
            return
        
        if self.direction == "left":
            self.image = player_image_left
        elif self.direction == "right":
            self.image = player_image_right
        elif self.direction == "up":
            self.image = player_image_back
        else:
            self.image = player_image
    
    def set_invincible(self, milliseconds=1000):
        self.invincible = True
        pygame.time.set_timer(INVINCIBLE_END, milliseconds, 1)

    def set_shooting(self):
        if not self.shooting:
            self.shooting = True
            self.with_bucket = False
            #self.bullets.append(Player.Bullet())
            pygame.time.set_timer(SHOOTING_END, 250, 1)
    
    def set_with_bucket(self):
        if self.with_bucket == False and player.colliderect(bucket):
            self.with_bucket = True
        elif self.with_bucket == True:
            self.with_bucket = False

    def set_bucket_action(self):
        if self.with_bucket == True:
            if self.colliderect(lake) and lake.full == True:
                bucket.full = True
                lake.start_recharge()
            elif bucket.full == True and self.colliderect(plant):
                bucket.full = False
                plant.xp += 1

class Noia(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, NOIA_WIDTH, NOIA_HEIGHT)
        self.image = noia_image
        self.velocity_y = 0
        self.velocity_x = 0
        self.direction = "down"
        self.health = 2

    def update_image(self):
        if self.direction == "left":
            self.image = noia_image_left
        elif self.direction == "right":
            self.image = noia_image_right
        elif self.direction == "up":
            self.image = noia_image_back
        else:
            self.image = noia_image 

class Plant(pygame.Rect):
    def __init__(self):
        super().__init__(PLANT_X, PLANT_Y, PLANT_WIDTH, PLANT_HEIGHT)
        self.image = plant_image1
        self.max_health = 10
        self.health = self.max_health
        self.direction = "right"
        self.level = 1
        self.xp = 0

    def update_image(self):
        if self.xp >= 3 and self.level == 1:
            self.level = 2
        if self.level == 1:
            self.image = plant_image1
        elif self.level == 2:
            self.image = plant_image2

class Lake(pygame.Rect):
    def __init__(self):
        super().__init__(LAKE_X, LAKE_Y, LAKE_WIDTH, LAKE_HEIGHT)
        self.image = lake_image_full
        self.full = True
        self.recharge_time = 5000 # milliseconds

    def update_image(self):
        if self.full == True:
            self.image = lake_image_full
        else:
            self.image = lake_image_empty
    
    def start_recharge(self):
        self.full = False
        # Inicia um timer único (1) que dispara o evento LAKE_RECHARGE após 'recharge_time'
        pygame.time.set_timer(LAKE_RECHARGE, self.recharge_time, 1)

class Bucket(pygame.Rect):
    def __init__(self):
        super().__init__(BUCKET_X, BUCKET_Y, BUCKET_WIDTH, BUCKET_HEIGHT)
        self.image = bucket_image_empty
        self.full = False

    def update_image(self):
        if self.full == True:
            self.image = bucket_image_full
        else:
            self.image = bucket_image_empty

def create_map():
    
    # noias
    noia1 = Noia(-70, -70)
    noias.append(noia1)

    noia2 = Noia(GAME_WIDTH + 10, plant.y)
    noias.append(noia2)

    noia3 = Noia(-60, GAME_HEIGHT + 20)
    noias.append(noia3)

def move():
    global noias

    # player x movement
    if player.direction == "left" and player.velocity_x < 0:
        player.velocity_x += FRICTION
    elif player.direction == "right" and player.velocity_x > 0:
        player.velocity_x -= FRICTION
    else:
        player.velocity_x = 0

    player.x += player.velocity_x
    if player.x < 0:
        player.x = 0
    elif player.x + player.width > GAME_WIDTH:
        player.x = GAME_WIDTH - player.width
    
    # player y movement
    if player.direction == "down" and player.velocity_y > 0:
        player.velocity_y -= FRICTION
    elif player.direction == "up" and player.velocity_y < 0:
        player.velocity_y += FRICTION
    else:
        player.velocity_y = 0

    player.y += player.velocity_y
    if player.y < 0:
        player.y = 0
    elif player.y + player.height > GAME_HEIGHT:
        player.y = GAME_HEIGHT - player.height

    # bucket 
    if player.with_bucket == True:
        bucket.x = player.x
        bucket.y = player.y + player.height  - bucket.height
    
    # enemy movement
    noias = [noia for noia in noias if noia.health > 0]

    for noia in noias:
        if noia.x < plant.x:
            noia.direction = "right"
            noia.x += NOIA_VELOCITY
        elif noia.x > plant.x:
            noia.direction = "left"
            noia.x -= NOIA_VELOCITY
        if noia.y < plant.y:
            noia.direction = "down"
            noia.y += NOIA_VELOCITY
        elif noia.y > plant.y:
            noia.direction = "up"
            noia.y -= NOIA_VELOCITY


# start game
player = Player()
plant = Plant()
lake = Lake()
bucket = Bucket()
noias = []

create_map()

def draw():
    window.blit(background_image, (0, 0))
    window.blit(player.image, (player.x, player.y))

    # lake
    lake.update_image()
    window.blit(lake.image, lake)
    
    # plant
    plant.update_image()
    window.blit(plant.image, plant)

    # enemies
    for noia in noias:
        noia.update_image()
        window.blit(noia.image, noia)

    # player and bucket
    player.update_image()
    bucket.update_image()
    
    if player.with_bucket == True and player.direction in ["left", "down", "right"]:
        window.blit(player.image, player)
        window.blit(bucket.image, bucket)
    else:
        window.blit(bucket.image, bucket)
        window.blit(player.image, player)

while True: # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == INVINCIBLE_END:
            player.invincible = False

        elif event.type == SHOOTING_END:
            player.shooting = False

        elif event.type == LAKE_RECHARGE:
            lake.full = True
            pygame.time.set_timer(LAKE_RECHARGE, 0)
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]):
        player.velocity_y = -PLAYER_VELOCITY
        player.direction = "up"
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.velocity_x = -PLAYER_VELOCITY
        player.direction = "left"

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.velocity_x = PLAYER_VELOCITY
        player.direction = "right"
        
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.velocity_y = PLAYER_VELOCITY
        player.direction = "down"

    if keys[pygame.K_x] or keys[pygame.K_SPACE]:
        player.set_shooting()
    
    if keys[pygame.K_e]:
        player.set_with_bucket()
    
    if keys[pygame.K_r]:
        player.set_bucket_action()

    move()
    draw()
    pygame.display.update()
    clock.tick(50) #60 frames per second (fps)