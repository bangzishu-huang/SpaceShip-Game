import pygame
from random import randint
# setting up
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spaceship Game :)")
run = True
clock = pygame.time.Clock()

surf = pygame.Surface((100,200))
x = 100

# importing graphics
player_surface = pygame.image.load('Code/Images/Spaceship.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (170,170))
player_rect = player_surface.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2()
player_speed = 250

star_surface = pygame.image.load('Code/Images/Star.png').convert_alpha()
star_surface = pygame.transform.scale(star_surface, (90,90))
star_position = [(randint(0, WINDOW_WIDTH), randint(0 , WINDOW_HEIGHT)) for i in range(25)]

meteor_surface = pygame.image.load('Code/Images/Meteor.png').convert_alpha()
meteor_surface = pygame.transform.scale(meteor_surface, (110,110))
meteor_rect = meteor_surface.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surface = pygame.image.load('Code/Images/Laser.png').convert_alpha()
laser_surface = pygame.transform.scale(laser_surface, (30, 80))
laser_rect = laser_surface.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

while run:
    dt = clock.tick() / 1000
    # print(clock.get_fps()) # checking fps

    # the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            player_rect.center = event.pos

    # user inputs
    key = pygame.key.get_pressed()
    player_direction.x = int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT])
    player_direction.y = int(key[pygame.K_DOWN]) - int(key[pygame.K_UP])
    player_direction = player_direction.normalize() if player_direction else player_direction
    player_rect.center += player_direction * player_speed * dt

    last_key = pygame.key.get_just_pressed()
    if last_key[pygame.K_SPACE]:
        print('Fire!')
    

    
    # draw
    screen.fill('light blue')

    for pos in star_position:
        screen.blit(star_surface, pos)

    screen.blit(meteor_surface, meteor_rect)
    screen.blit(laser_surface, laser_rect)

    
    player_rect.center += player_direction * player_speed * dt
    screen.blit(player_surface, player_rect)

    pygame.display.update()

pygame.quit()
