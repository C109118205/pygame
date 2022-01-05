import pygame,os
from pygame import key
import random
import re
import db_config
from pygame import font
from pygame import draw
from pygame.event import wait

WIDTH = 500
HEIGHT = 600
WHITE = (255,255,255)
GREEN =(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)
BLACK=(0,0,0)
FPS=60

#遊戲初始化
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("FPSgame")
clock = pygame.time.Clock()


#載入圖片
# print (os.path.join("img","background.png"))
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())
#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.05)


font_name = os.path.join("font.ttf")
def draw_text(surf, text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def new_rock():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

def draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_init():
    global running
    width = 600
    height = 300
    color_background = (0, 0, 0)
    color_inactive = (100, 100, 200)
    color_active = (200, 200, 255)
    color_inactive2 = (100, 100, 200)
    color_active2 = (200, 200, 255)
    color = color_inactive
    color2 = color_inactive2

    font = pygame.font.Font(None, 32)
    button_color = (200,200,200)
    button_text = font.render("login", True, button_color)
    button_clicked = font.render("Clicked", True, button_color)
    button_rect = pygame.Rect(200, 200, 60, 30)
    
    Quit_button_text = font.render("QUIT", True, button_color)
    Quit_button_clicked = font.render("QUIT_Clicked", True, button_color)
    Quit_button_rect = pygame.Rect(20, 550, 60, 25)

    register_button_text = font.render("Register", True, button_color)
    register_button_clicked = font.render("Register_Clicked", True, button_color)
    register_button_rect = pygame.Rect(300, 200, 100, 30)

    select_score_button_text = font.render("score", True, button_color)
    select_score_button_clicked = font.render(" select score Clicked", True, button_color)
    select_score_button_rect = pygame.Rect(100, 200, 65, 30)

    global user,password,message,get_score
    passowrd = ""
    user = ""
    message = ""
    get_score=['']

    active = False
    active1 = False

    
    input_box = pygame.Rect(100, 100, 140, 32)
    input_box2 = pygame.Rect(100, 100, 140, 32)

    pygame.display.update()

    waiting = True

    while waiting:
        clock.tick(FPS) #更新畫面FPS
    #取得輸入
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #     elif event.type == pygame.KEYUP:
        #         waiting = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return running
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = True if input_box.collidepoint(event.pos) else False
                active1 = True if input_box2.collidepoint(event.pos) else False
                # Change the current color of the input box
                color = color_active if active else color_inactive
                color2 = color_active2 if active1 else color_inactive2

            if event.type == pygame.MOUSEBUTTONUP:
                button_clicked = True if button_rect.collidepoint(event.pos) else False
                Quit_button_clicked = True if Quit_button_rect.collidepoint(event.pos) else False
                register_button_clicked = True if register_button_rect.collidepoint(event.pos) else False
                select_score_button_clicked = True if select_score_button_rect.collidepoint(event.pos) else False
                
                if select_score_button_clicked:
                    # message = str(db_config.select_score(user))
                    # print(message)
                    for i in db_config.select_score(user):
                        meg = re.sub(r"[^a-zA-Z0-9]","",str(i))
                        message = "{}{}{}".format(user," score is:",meg)
                        get_score.append(message)

                if Quit_button_clicked:
                    waiting = False
                    running = False
                    return running

                if register_button_clicked:
                    db_config.register(user,passowrd)

                if button_clicked:     
                    if db_config.login(user,passowrd) == 1:
                        waiting=False
                    else:
                        waiting=True

            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        print(user)
                    elif event.key == pygame.K_BACKSPACE:
                        user = user[:-1]
                    else:
                        user += event.unicode
                if active:
                    if event.key == pygame.K_RETURN:
                        print(passowrd)

                    elif event.key == pygame.K_BACKSPACE:
                        passowrd = passowrd[:-1]
                    else:
                        passowrd += event.unicode

        # Input box
        text_surface = font.render(passowrd, True, color)
        text_surface2 = font.render(user, True, color2)

        input_box_width = max(200, text_surface.get_width()+10)
        input_box_width2 = max(200, text_surface2.get_width()+10)

        input_box.w = input_box_width
        input_box2.w = input_box_width2
        input_box.center = (width/2, height/2)
        input_box2.center = (width/2, height/2.5)

        # Updates
        screen.fill(color_background)
        screen.blit(background_img,(0,0))
        screen.blit(button_text,button_rect)
        screen.blit(Quit_button_text,Quit_button_rect)
        screen.blit(register_button_text,register_button_rect)
        screen.blit(select_score_button_text,select_score_button_rect)

        screen.blit(text_surface, (input_box.x+5, input_box.y+5))
        screen.blit(text_surface2, (input_box2.x+5, input_box2.y+5))

        pygame.draw.rect(screen, color, input_box, 3)
        pygame.draw.rect(screen, color2, input_box2, 3)
        pygame.draw.rect(screen, button_color, button_rect, 2)
        pygame.draw.rect(screen, button_color, Quit_button_rect, 2)
        pygame.draw.rect(screen, button_color, register_button_rect, 2)
        pygame.draw.rect(screen, button_color, select_score_button_rect, 2)


        for i in range(len(get_score)):
            draw_text(screen,str(get_score[i]),32,(WIDTH/2),200+i*50)

        # draw_text(screen,'AD左右移動飛船 space發射子彈',22,WIDTH/2,HEIGHT/2)
        # draw_text(screen,'按任意鍵開始遊戲!',18,WIDTH/2,HEIGHT*3/4)
        pygame.display.flip()
def end_init():
    end=True

    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
        screen.fill(BLACK)
        screen.blit(background_img,(0,0))
        all_sprites.draw(screen)
        pygame.display.update()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 8
        self.health =100

    def update(self):
        key_pressed = pygame.key.get_pressed() #key get event
        if key_pressed[pygame.K_d]:
            self.rect.x +=self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -=self.speedx

        #判斷是否碰到牆
        if self.rect.right > WIDTH:
            self.rect.right =WIDTH    
        if self.rect.left <0:
            self.rect.left =0
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs) 
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *0.85 / 2)
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)
     
    #轉動圖片 
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori,self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
global score
for i in range(8):
    new_rock()
score = 0
pygame.mixer.music.play(-1)
show_init = True

running = True


while running:
    if show_init:
        draw_init()
        show_init = False
    clock.tick(FPS) #更新畫面FPS
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #更新畫面
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        new_rock()


    hits = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius        
        new_rock()

        if player.health <= 0:
            db_config.create_score(user,score)   
            running = False
    
    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.health,5,15)
    pygame.display.update()
pygame.quit()