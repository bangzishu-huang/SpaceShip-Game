import pygame

# setting up
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spaceship Game :)")
run = True

surf = pygame.Surface((100,200))

# the loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill('light blue')
    screen.blit(surf, (100, 150))
    pygame.display.update()

pygame.quit()
