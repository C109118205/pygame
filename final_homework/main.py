import pygame,os
from pygame import key
import random

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
    text = ""
    text2 = ""

    active = False
    active1 = False

    waiting = True
    
    input_box = pygame.Rect(100, 100, 140, 32)
    input_box2 = pygame.Rect(100, 100, 140, 32)

    pygame.display.update()

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
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = True if input_box.collidepoint(event.pos) else False
                active1 = True if input_box2.collidepoint(event.pos) else False

                # Change the current color of the input box
                color = color_active if active else color_inactive
                color2 = color_active2 if active1 else color_inactive2

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                if active1:
                    if event.key == pygame.K_RETURN:
                        print(text2)
                        text2 = ""
                        waiting = False
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        # Input box
        text_surface = font.render(text, True, color)
        text_surface2 = font.render(text2, True, color2)

        input_box_width = max(200, text_surface.get_width()+10)
        input_box_width2 = max(200, text_surface2.get_width()+10)

        input_box.w = input_box_width
        input_box2.w = input_box_width2
        input_box.center = (width/2, height/2)
        input_box2.center = (width/2, height/2.5)

        # Updates
        screen.fill(color_background)
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))
        screen.blit(text_surface2, (input_box2.x+5, input_box2.y+5))
        pygame.draw.rect(screen, color, input_box, 3)
        pygame.draw.rect(screen, color2, input_box2, 3)
        # draw_text(screen,'C109118205羅志文',32,WIDTH/2,HEIGHT/4)
        # draw_text(screen,'AD左右移動飛船 space發射子彈',22,WIDTH/2,HEIGHT/2)
        # draw_text(screen,'按任意鍵開始遊戲!',18,WIDTH/2,HEIGHT*3/4)
        pygame.display.flip()

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
            running = False
    
    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.health,5,15)
    pygame.display.update()
pygame.quit()