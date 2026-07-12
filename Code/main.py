import pygame
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('Code/Images/Spaceship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (170,170))
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 320

        self.shoot = True
        self.laser_shot_time = 0
        self.cooldown = 400
        self.mask = pygame.mask.from_surface(self.image)

    def laser_time(self):
        if not self.shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shot_time >= self.cooldown:
                self.shoot = True

    def update(self, dt):
        # user input
        key = pygame.key.get_pressed()
        self.direction.x = int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT])
        self.direction.y = int(key[pygame.K_DOWN]) - int(key[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        last_key = pygame.key.get_just_pressed()
        if last_key[pygame.K_SPACE] and self.shoot:
            laser_spawn_pos = (self.rect.midtop[0], self.rect.midtop[1] + 48)
            Laser(laser_surface, laser_spawn_pos, (all_sprites, laser_sprites))
            self.shoot = False
            self.laser_shot_time = pygame.time.get_ticks()

        self.laser_time()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH),randint(0 , WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image, (20, 60))
        self.rect = self.image.get_frect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.rect.centery -= 400 * dt
        
        # ensuring no sprite overload
        if self.rect.bottom < 0:
            self.kill

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = self
        self.image = pygame.transform.scale(meteor_surface, (120,120))
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.life = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(380, 460)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life:
            self.kill

def collision():
    global run

    collision = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision:
        run = False

    for laser in laser_sprites:
        collided = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)
        if collided:
            laser.kill()


# setting up
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spaceship Game :)")
run = True
clock = pygame.time.Clock()


# importing surfaces
star_surf = pygame.image.load('Code/Images/Star.png').convert_alpha()
laser_surface = pygame.image.load('Code/Images/Laser.png').convert_alpha()
meteor_surface = pygame.image.load('Code/Images/Meteor.png').convert_alpha()


# some sprites 
surf = pygame.Surface((100,200))
x = 100

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


# meteors stuff
meteor_run = pygame.event.custom_type()
pygame.time.set_timer(meteor_run, 600)


while run:
    dt = clock.tick() / 1000
    # print(clock.get_fps()) # checking fps

    # the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == meteor_run:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surface, (x, y), (all_sprites, meteor_sprites))
    
    # updating the game
    all_sprites.update(dt)
    collision()
    
    # draw
    screen.fill('#263652')
    all_sprites.draw(screen)

    pygame.display.update()

pygame.quit()
