import os
import pygame
import random
from pygame import *
import time
#screen setup
pygame.init()
scr_size = (width, height) = (800, 400)
FPS = 60
gravity = 0.6
screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Cheetos_Run by Nata")
pygame.display.set_icon(pygame.image.load('sprites/cheetoslogo.png'))

#color setup
black = (0, 0, 0)
white = (255, 255, 255)
background_col = (176, 196, 230)
yellow = (255, 255, 0)
red = (250, 0, 0)
green = (0, 255, 0)
blue = (50, 153, 213)
cream = (255, 239, 213)
purple = (204, 204, 255)
bluegreen = (0, 153, 153)
darkgreen = (0, 51, 51)
lightblue = (0, 255, 255)

#highscore setup
highscore_file = open('cheetos_highscore.txt', 'r')
highscore = int(highscore_file.read())
first_highscore = highscore
highscore_file.close()

#font setep
pygame.font.init()
font1 = pygame.font.Font('sprites/Cactus Cuties.ttf', 58)
font2 = pygame.font.Font('sprites/HelloDoodles.ttf', 56)
font3 = pygame.font.Font('sprites/Phonics-Bats-by-Phontz.ttf', 56)
font4 = pygame.font.Font('sprites/Distro2 Bats.ttf', 65)
font5 = pygame.font.Font('sprites/PIZZADUDEBULLETS.ttf', 55)
font6 = pygame.font.Font('sprites/Sushi Sushi.ttf', 55)
font7 = pygame.font.Font('sprites/Rakugaki.ttf', 55)
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)

#sound setup
pygame.mixer.init()
click = pygame.mixer.Sound('sprites/click.mp3')
spark = pygame.mixer.Sound('sprites/spark.mp3')
countdown_beep = pygame.mixer.Sound('sprites/countdown_beep.wav')
bonus_recieve = pygame.mixer.Sound('sprites/snake_eat.wav')  #eat,pop,drip,bite,pop_hollow,snake_eat
tick_sound = pygame.mixer.Sound('sprites/tick.mp3')
tock_sound = pygame.mixer.Sound('sprites/tock.mp3')
jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')
verse_sound = pygame.mixer.Sound('sprites/verse.mp3')
bp_sound = pygame.mixer.Sound('Sprites/bp.wav')
gameover = pygame.mixer.Sound('Sprites/gameover.wav')
bg_sound = pygame.mixer.Sound('Sprites/music_zapsplat_game_music_fun_tropical_caribean_steel_drums_percussion_008.mp3')

#snake_setup
snake_block = 10
snake_speed = 10

#memory_setup
pad = 9
nsymb = 6
row, col = 6, 6
ntiles = row * col
tile_h, tile_w = 56, 56

def load_image(name, sizex=-1, sizey=-1, colorkey = None,):

    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(sheetname, nx, ny, scalex = -1, scaley = -1, colorkey = None,):
    fullname = os.path.join('sprites', sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0, ny):
        for j in range(0, nx):
            rect = pygame.Rect((j*sizex, i*sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image, (scalex, scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect

def disp_gameOver_msg(retbutton_image, gameover_image):
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = width / 2
    retbutton_rect.top = height / 2
    screen.blit(retbutton_image, retbutton_rect)
    #gameover_rect = gameover_image.get_rect()
    #gameover_rect.centerx = width / 2
    #gameover_rect.centery = height*0.43
    #screen.blit(gameover_image, gameover_rect)
    font_gameover = pygame.font.Font('sprites/half_bold_pixel-7.ttf', 22)
    gameover_text = font_gameover.render('G  A  M  E    O  V  E  R', True, black)
    screen.blit(gameover_text, [width * 0.27, height * 0.41])
    bg_sound.stop()
    pygame.display.update()

def extractDigits(number):
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number % 10)
            number = int(number/10)

        #digits.append(number % 10)
        for i in range(len(digits), 5):
            digits.append(0)
        digits.reverse()
        return digits

class Dino():
    def __init__(self, sizex=-1, sizey=-1):
        self.images, self.rect = load_sprite_sheet('dino.png', 5, 1, sizex, sizey, -1)
        self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, sizey, -1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        screen.blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.isDead:
           self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index) % 2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = (self.counter + 1)

class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex =-1, sizey =-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('cacti-small.png', 3, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0, 3)]
        self.movement = [-1*speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

class Bonus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('bonusp.png', 1, 1, sizex, sizey, -1)
        self.bonus_height = [height * 0.75, height * 0.83, height * 0.9]
        self.rect.centery = self.bonus_height[random.randrange(0, 3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1 * speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

class Ptera(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('ptera.png', 2, 1, sizex, sizey, -1)
        self.ptera_height = [height*0.82, height*0.75, height*0.60]
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()

class Ground():
    def __init__(self, speed=-5):
        self.image, self.rect = load_image('ground.png', -1, -1, -1)
        self.image1, self.rect1 = load_image('ground.png', -1, -1, -1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image('cloud.png', int(120*40/42), 50, -1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()

class Scoreboard():
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11*6/5), -1)
        self.image = pygame.Surface((55, int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width*0.9
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.04
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, score):
        score_digits = extractDigits(score)
        self.image.fill(background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s], self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0

def introscreen():
    temp_dino = Dino(44, 47)
    temp_dino.isBlinking = True
    gameStart = False

    temp_ground, temp_ground_rect = load_sprite_sheet('ground.png', 15, 1, -1, -1, -1)
    temp_ground_rect.left = width/20
    temp_ground_rect.bottom = height

    font_style = pygame.font.SysFont("comicsansms", 40)
    text = font_style.render('welcome to', True, white)
    screen.blit(text, (20, 20))
    logo, logo_rect = load_image('cheetos2.png', 546, 291, -1)
    logo_rect.centerx = width * 0.555
    logo_rect.centery = height * 0.5
    cnt_jump = 0

    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if pygame.key == pygame.K_ESCAPE:
                        return True
                    else:
                        if cnt_jump < 1:
                            temp_dino.isJumping = True
                            temp_dino.isBlinking = False
                            temp_dino.movement[1] = -1 * temp_dino.jumpSpeed
                            cnt_jump += 1

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)
            screen.blit(temp_ground[0], temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo, logo_rect)
                font_c = pygame.font.Font('sprites/dogicapixel.ttf', 18)
                cheetos = font_c.render("PRESS ANY KEY TO START !", True, white)
                screen.blit(cheetos, [275, 310])
            temp_dino.draw()

            pygame.display.update()

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True
            bg_sound.set_volume(0.2)
            bg_sound.play(-1)

def backtorun(text, x, y, t):
    font_c = pygame.font.Font('sprites/dogicapixel.ttf', 18)
    cheetos = font_c.render(text, True, white)
    screen.blit(cheetos, [x, y])
    pygame.display.update()
    time.sleep(t)

def changescreen(bp):
    screen.blit(pygame.image.load("sprites/ch1.png"), (0, 0))
    backtorun('YOU RECIEVE  + ' + str(bp) + '  BONUS POINT', 200, 100, 3)
    screen.blit(pygame.image.load("sprites/ch1.png"), (0, 0))
    backtorun('GOING BACK TO RUN', 280, 100, 1)
    screen.blit(pygame.image.load("sprites/ch2.png"), (0, 0))
    backtorun('IN', 380, 100, 0.5)
    screen.blit(pygame.image.load("sprites/ch3.png"), (0, 0))
    backtorun('3', 380, 100, 0.4)
    screen.blit(pygame.image.load("sprites/ch4.png"), (0, 0))
    backtorun('3', 380, 100, 0.4)
    screen.blit(pygame.image.load("sprites/ch5.png"), (0, 0))
    backtorun('2', 380, 100, 0.4)
    screen.blit(pygame.image.load("sprites/ch6.png"), (0, 0))
    backtorun('2', 380, 100, 0.4)
    screen.blit(pygame.image.load("sprites/ch7.png"), (0, 0))
    backtorun('1', 380, 100, 0.4)
    screen.blit(pygame.image.load("sprites/ch8.png"), (0, 0))
    backtorun('1', 380, 100, 0.4)

def Your_score(score):
    value = score_font.render("Bonus Point + " + str(score*20), True, yellow)
    screen.blit(value, [15, 10])
    global Score
    Score = score*20

def snake_time(time_left):
    if time_left > 60 and time_left % 20 == 0:
        tock_sound.play()
    elif time_left > 60 and time_left % 20 == 10:
        tick_sound.play()
    elif time_left <= 60 and time_left % 10 == 0:
        tick_sound.play()
    elif time_left <= 60 and time_left % 10 == 5:
        tock_sound.play()
    Text = score_font.render("Time left: "+str(int(time_left/10))+' s', True, red)
    screen.blit(Text, (600, 10))

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, red, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 5, height / 2.5])

def snakeLoop():
    global bp
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, 790) / 10.0) * 10.0
    foody = round(random.randrange(60, 390) / 10.0) * 10.0

    t = 610

    while not game_over:

        while game_close == 1:
            Your_score(Length_of_snake - 1)
            bp = Score
            game_over = True
            game_close = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_ESCAPE:
                    game_over = True

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.blit(pygame.image.load("sprites/space_background.png"), (0, 0))
        pygame.draw.rect(screen, random.choice([green, lightblue]), [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        snake_time(t-1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(790) / 10.0) * 10.0
            foody = round(random.randrange(60, 390) / 10.0) * 10.0
            Length_of_snake += 1
            bonus_recieve.play()

        t -= 1
        if t == 0:
            Your_score(Length_of_snake - 1)
            bp = Score
            game_over = True

        clock.tick(10)
    return bp

class Tile:
    def __init__(self, i, j, symb):
        self.symb = symb
        self.reveal = False
        self.matched = False
        x = (i + 1) * pad + i * tile_w
        y = (j + 1) * pad + j * tile_h
        self.rect = pygame.Rect(x, y, tile_w, tile_h)

    def hide(self):
        self.reveal = False

    def show(self):
        self.reveal = True
        textSurf = font.render(self.__repr__(), True, darkgreen)
        screen.blit(textSurf, self.rect.topleft)

    def __repr__(self):
        return str(self.symb) if self.reveal else "*"

def refresh(tiles, start = False):
    for tile in tiles:
        if start or tile.reveal and not tile.matched:
            tile.hide()
            pygame.draw.rect(screen, bluegreen, tile.rect)

def keep(shown, tile, index):
    shown.append(index)
    tile.matched = True

def memory_time(time_left):
    if time_left > 300 and time_left % 120 == 0:
        tock_sound.play()
    elif time_left > 300 and time_left % 120 == 60:
        tick_sound.play()
    elif time_left <= 300 and time_left % 60 == 0:
        tick_sound.play()
    elif time_left <= 300 and time_left % 60 == 30:
        tock_sound.play()
    pygame.font.init()
    Text = score_font.render("Time left: " + str(int(time_left / 60)) + ' s  ', True, red, black)
    screen.blit(Text, (500, 350))

def memoryLoop():
    global Score, bp, font
    Score = 0
    t = 3660

    font = random.choice([font1, font2, font3, font4, font5, font6, font7])

    text = score_font.render('Bonus Point + ', True, yellow)
    screen.blit(text, (420, 15))

    text = score_font.render(str(Score), True, yellow)
    screen.blit(text, (580, 15))

    c, r, s = range(col), range(row), range(nsymb)
    symbs = [i for i in s for j in range(int(ntiles / nsymb))]
    random.shuffle(symbs)
    tiles = [Tile(i, j, symbs[i + j * col]) for j in r for i in c]
    shown = []
    refresh(tiles, True)

    while len(shown) < ntiles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                loc = event.__dict__['pos']
                for i, tile in enumerate(tiles):
                    if tile.rect.collidepoint(loc):
                        tile.show()
                        click.play()
                        pygame.display.update()
                        if i not in shown:
                            if len(shown) % 2 == 1:
                                j = shown.pop()
                                prev = tiles[j]
                                if tile.symb == prev.symb:
                                    keep(shown, tile, i)
                                    keep(shown, prev, j)
                                    Score += 20
                                    spark.play()
                                    text = font_style.render(str(Score), True, yellow, black)
                                    screen.blit(text, (580, 15))
                                    bp = Score
                                    pygame.display.update()
                                else:
                                    time.sleep(0.5)
                                    t -= 29
                                    refresh(tiles)
                            else:
                                shown.append(i)
        memory_time(t - 1)
        pygame.display.update()
        t -= 1
        if t <= 0:
            return bp
        pygame.init()
        pygame.display.update()
        clock.tick(60)

    text = font_style.render('Complete!', True, yellow)
    screen.blit(text, (525, 200))
    pygame.display.update()
    time.sleep(2)
    return bp

def gameplay():
    global bp, highscore
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    playerDino = Dino(44, 47)
    new_ground = Ground(-1*gamespeed)
    scb = Scoreboard()
    counter = 0
    highsc = Scoreboard(51)

    cacti = pygame.sprite.Group()
    bonus = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Bonus.containers = bonus
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbutton_image, retbutton_rect = load_image('replay_button.png', 60, 50, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 280, 15, -1)

    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
    HI_image = pygame.Surface((22, int(11 * 6 / 5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = 16
    HI_rect.left = 22

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                            if playerDino.rect.bottom == int(0.98*height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            playerDino.isDucking = False

            for c in cacti:
                c.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino, c):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        gameover.play()

            for p in pteras:
                p.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino, p):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        gameover.play()

            for b in bonus:
                b.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino, b):
                    b.movement[0] = -20 * gamespeed
                    verse_sound.play()
                    screen.fill(black)
                    pygame.display.update()
                    time.sleep(1)
                    if random.randrange(2) == 1:
                        bp = memoryLoop()
                    else:
                        bp = snakeLoop()
                    playerDino.score += bp
                    changescreen(bp)
                    scb.update(playerDino.score)
                    verse_sound.play()
                    bp = 0

            if len(cacti) < 2:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed, 40, 40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0, 50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))

            if len(bonus) == 0 and counter > 500 and playerDino.score % 200 <= 10:
                for l in last_obstacle:
                    if l.rect.right < width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Bonus(gamespeed, 46, 40))

            if len(pteras) == 0 and random.randrange(0, 200) == 10 and counter > 500:
                for l in last_obstacle:
                    if l.rect.right < width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Ptera(gamespeed, 46, 40))

            if len(clouds) < 5 and random.randrange(0, 300) == 10:
                Cloud(width, random.randrange(height/5, height/2))

            playerDino.update()
            cacti.update()
            bonus.update()
            pteras.update()
            clouds.update()
            new_ground.update()
            scb.update(playerDino.score)
            highsc.update(highscore)

            if pygame.display.get_surface() != None:
                screen.fill(background_col)
                new_ground.draw()
                clouds.draw(screen)
                scb.draw()
                if highscore != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                cacti.draw(screen)
                bonus.draw(screen)
                pteras.draw(screen)
                playerDino.draw()
                pygame.display.update()
            clock.tick(FPS)

            if playerDino.isDead:
                gameOver = True

            if counter % 800 == 799:
                new_ground.speed -= 0.4
                gamespeed += 0.4

            if playerDino.score > highscore:
                highscore = playerDino.score

            counter += 1

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            main()
            highsc.update(highscore)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(retbutton_image, gameover_image)
                if highscore != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                pygame.display.update()
            clock.tick(FPS)
    newhigh = open('cheetos_highscore.txt', 'w')
    newhigh.write(str(highscore))
    newhigh.close()
    pygame.quit()
    quit()

def main():
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay()

main()
newhigh = open('cheetos_highscore.txt', 'w')
newhigh.write(str(highscore))
newhigh.close()
