import pygame
from random import randint, uniform, choice
import asyncio

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('Images/Spaceship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (110,110))
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 320
        self.mode = 'keyboard'

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
        if self.mode == 'keyboard':
            key = pygame.key.get_pressed()
            self.direction.x = int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT])
            self.direction.y = int(key[pygame.K_DOWN]) - int(key[pygame.K_UP])
            self.direction = self.direction.normalize() if self.direction else self.direction
            self.rect.center += self.direction * self.speed * dt

            # last_key = pygame.key.get_just_pressed()
            # if last_key[pygame.K_SPACE] and self.shoot:
            #     self.fire_laser()


        
        elif self.mode == 'mouse':
            self.rect.center = pygame.mouse.get_pos()

            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] and self.shoot:
                self.fire_laser()

        self.laser_time()

    def fire_laser(self):
        laser_spawn_pos = (self.rect.midtop[0], self.rect.midtop[1] + 10)
        Laser(laser_surface, laser_spawn_pos, (all_sprites, laser_sprites))
        self.shoot = False
        self.laser_shot_time = pygame.time.get_ticks()
        laser_sound.play()

class Star(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.life = 3000
        self.speed = 100
        self.direction = pygame.Vector2(0,1)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life:
            self.kill

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
        self.image = surf
        self.image = pygame.transform.scale(meteor_surface, (120,120))
        self.og = self.image
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.life = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(35,85) * choice([-1, 1])
        self.angle = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life:
            self.kill()
        self.angle += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.og, self.angle, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Boom(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frames_index += 25 * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else:
            self.kill()

def collision():
    global run, hit_count, game_state
    
    hit = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if hit:
        player_death()

    for laser in laser_sprites:
        collided = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)
        if collided:
            hit_count += len(collided)
            laser.kill()
            Boom(boom_frames, laser.rect.midtop, all_sprites)
            boom_sound.play()

def player_death():
    global game_state

    bgm_sound.stop()
    damage_sound.play()
    Boom(boom_frames, player.rect.center, all_sprites)
    player.kill()
    game_state = 'dying'

    for m in meteor_sprites:
        m.kill()
    for l in laser_sprites:
        l.kill()

def score():
    time_now = (pygame.time.get_ticks() - game_start) // 1000
    text_surface = font.render(f'Time survived: {str(time_now)} | Hit: {hit_count}', True, '#F0F6FF')
    text_rect = text_surface.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    screen.blit(text_surface, text_rect)
    pygame.draw.rect(screen, '#F0F6FF', text_rect.inflate(20,20).move(0, +2), 5, 10)

def draw_menu():
    screen.fill('#7EAFCF')
    title_surface = font.render('Spaceship Game!', True, '#D5DDED')
    title_rect = title_surface.get_frect(center = (WINDOW_WIDTH / 2, 150))
    screen.blit(title_surface, title_rect)

    mouse_pos = pygame.mouse.get_pos()
    option_rects = []

    for i, option in enumerate(menu):
        option_surface = font.render(option, True, '#BAC7D1')
        option_rect = option_surface.get_frect(center = (WINDOW_WIDTH / 2, 300 + i * 100))
        hover = option_rect.inflate(30, 20).collidepoint(mouse_pos)
        color = '#D1D8E0' if hover == selected else '#BAC7D1'
        option_surface = font.render(option, True, color)
        screen.blit(option_surface, option_rect)
        pygame.draw.rect(screen, '#D1D8E0', option_rect.inflate(30, 20), 4, 10)
        
        option_rects.append(option_rect.inflate(30, 20))

    last_y = 300 + (len(menu) - 1) * 100
    hint_font = pygame.font.Font('Images/Lexend-Bold.ttf', 20)
    hint_surface = hint_font.render('Arrow keys to move, Space to shoot (for keyboard)', True, '#D3E4F2')
    hint_rect = hint_surface.get_frect(center = (WINDOW_WIDTH / 2, last_y + 80))
    screen.blit(hint_surface, hint_rect)
        
    
    return option_rects

def esp():
    
    # outlining meteor and showing their distance
    for meteor in meteor_sprites:
        pygame.draw.rect(screen, '#FF4D4D', meteor.rect, 4)
        pygame.draw.line(screen, '#FF4D4D', player.rect.center, meteor.rect.center, 2)
        distance = int(pygame.Vector2(player.rect.center).distance_to(meteor.rect.center))
        font = pygame.font.Font('Images/Lexend-Bold.ttf', 16)
        distance_surface = font.render(str(distance), True, '#FF4D4D')
        distance_rect = distance_surface.get_frect(midtop=meteor.rect.midbottom)
        screen.blit(distance_surface, distance_rect)
    
    #outlining player
    pygame.draw.rect(screen, "#A1FF92", player.rect, 4)

def reset_game():
    global player, hit_count, game_start, target_mode, meteor_spawn, star_spawn

    target_mode = False
    meteor_spawn = pygame.time.get_ticks()
    star_spawn = pygame.time.get_ticks()
    game_start = pygame.time.get_ticks()
    all_sprites.empty()
    meteor_sprites.empty()
    laser_sprites.empty()
    star_sprites.empty()

    hit_count = 0
    player = Player(all_sprites)
    for i in range(10):
        x, y =  randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
        Star((star_surf), (x, y), star_sprites)

    bgm_sound.play(loops = -1)

# setting up
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spaceship Game :)")
run = True
clock = pygame.time.Clock()
hit_count = 0
game_start = pygame.time.get_ticks()
game_menu = 'menu'
selected = 0
menu = ['Play with Keyboard', 'Play with Mouse', 'Target Mode?']
current_menu = []
game_state = 'menu'
target_mode = False


# importing stuff
star_surf = pygame.image.load('Images/Star.png').convert_alpha()
star_surf.fill((213, 216, 237, 0), special_flags=pygame.BLEND_RGBA_ADD)
laser_surface = pygame.image.load('Images/Laser.png').convert_alpha()
meteor_surface = pygame.image.load('Images/Meteor.png').convert_alpha()
font = pygame.font.Font('Images/Lexend-Bold.ttf', 44)
boom_frames = [pygame.image.load(f'Images/Boom/{i}.png').convert_alpha() for i in range(21)]
for frame in boom_frames:
    frame.fill((117, 186, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)
laser_sound =  pygame.mixer.Sound('Audio/laser.ogg')
laser_sound.set_volume(0.8)
boom_sound =  pygame.mixer.Sound('Audio/boom.ogg')
damage_sound =  pygame.mixer.Sound('Audio/damage.ogg')
bgm_sound =  pygame.mixer.Sound('Audio/bgm.ogg')
bgm_sound.set_volume(0.4)
bgm_sound.play(loops = -1)

# some sprites 
surf = pygame.Surface((100,200))
x = 100

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
star_sprites = pygame.sprite.Group()

player = Player(all_sprites)

# prefill some stars
for i in range (10):
    x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
    Star(star_surf, (x, y), star_sprites)

# showering down stuff
meteor_spawn = pygame.time.get_ticks()
meteor_interval = 500

star_spawn = pygame.time.get_ticks()
star_interval = 1200

async def main():
    global run, game_state, current_menu, target_mode, meteor_spawn, star_spawn

    while run:
        dt = clock.tick() / 1000
        # print(clock.get_fps()) # checking fps

        # the loop
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            # menu options
            if event.type == pygame.KEYDOWN and game_state == 'game':
                if event.key == pygame.K_SPACE and player.mode == 'keyboard' and player.shoot:
                    player.fire_laser()

            if event.type == pygame.MOUSEBUTTONDOWN and game_state == 'menu':
                for i, rect in enumerate(current_menu):
                    if rect.collidepoint(event.pos):
                        if i == 0:
                            player.mode = 'keyboard'
                            target_mode = False
                            game_state = 'game'
                        elif i == 1:
                            player.mode = 'mouse'
                            target_mode = False
                            game_state = 'game'
                        elif i == 2:
                            player.mode = 'keyboard'
                            target_mode = True
                            game_state = 'game'
        
        # updating the game
        if game_state == 'menu':
            current_menu = draw_menu()
        elif game_state == 'game':
            star_sprites.update(dt)
            all_sprites.update(dt)
            collision()
            current_time = pygame.time.get_ticks()

            if current_time - meteor_spawn >= meteor_interval:
                meteor_spawn = current_time
                x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                Meteor(meteor_surface, (x, y), (all_sprites, meteor_sprites))
            if current_time - star_spawn >= star_interval:
                star_spawn = current_time
                for i in range(randint(2,4)):
                    x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                    Star(star_surf, (x, y), star_sprites)
            screen.fill('#263652')
            score()
            star_sprites.draw(screen)
            all_sprites.draw(screen)
            if target_mode:
                esp()
        elif game_state == 'dying':
            all_sprites.update(dt)
            screen.fill('#263652')
            star_sprites.draw(screen)
            all_sprites.draw(screen)
            if not any(isinstance(s, Boom) for s in all_sprites):
                reset_game()
                game_state = 'menu'

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())