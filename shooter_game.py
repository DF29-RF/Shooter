from pygame import *
from random import *
from time import time as get_time

SCREEN_SIZE = (700, 500)
SPRITE_SIZE = 65
FPS = 60
WHITE = (255, 255, 255)

font.init()  

def show_text(x, y, text, color,fsize=50):
    label = font.Font(None, fsize).render(text, True, color)
    window.blit(label, (x, y))

class Counter:
    def __init__(self, x, y, text, font_size=40):
        self.pos = (x, y)
        self.text = text
        self.count = 0
        self.font = font.SysFont('Arial', font_size)
        self.render()

    def render(self):
        self.image = self.font.render(self.text + str(self.count), True, WHITE)

    def show(self):
        window.blit(self.image, self.pos)
class GameSprite(sprite.Sprite):
    def __init__(self, x, y, image_name, speed, scale=1):
        super().__init__()
        self.image = transform.scale(image.load(image_name),(SPRITE_SIZE// scale, SPRITE_SIZE // scale))    
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

bullets = sprite.Group()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_SIZE[1]:
            self.rect.y = 0 
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            missed_counter.count += 1
            missed_counter.render()
        self.show()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_SIZE[1]:
            self.rect.y = 0 
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)

asteroids = sprite.Group()
for _ in range(2):
    asteroids.add(Asteroid(randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, 'asteroid.png', 3))

class Player(GameSprite):
    def __init__(self, x, y, image_name, speed, scale=1):
        super().__init__(x, y, image_name, speed, scale)
        self.amount_bullets = 100     

        self.last_shoot_time = 0
        self.lives = 3
        self.img_live = transform.scale(image.load(image_name),(SPRITE_SIZE// (scale*2), SPRITE_SIZE // (scale*2)))  
    def move(self):
        pressed = key.get_pressed()
        if pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if pressed[K_d] and self.rect.x < SCREEN_SIZE[0] - self.rect.width:
            self.rect.x += self.speed
        if pressed[K_w] and self.rect.y:
            self.rect.y -= self.speed
        if pressed[K_SPACE] and self.amount_bullets > 0:
            if get_time() - self.last_shoot_time >= .5:
                self.shoot()
                self.last_shoot_time = get_time()
            
    def shoot(self):
        bullet1 = Bullet(self.rect.x, self.rect.y, 'bullet.png', 5, 4)
        bullet1.rect.x += int(1.5 * bullet1.rect.width)
        bullets.add(bullet1)
        self.amount_bullets -= 2
        mixer.Sound('fire.ogg').play()
        b1 = Bullet(self.rect.x, self.rect.y, 'bullet.png', 5, 4)
        bullets.add(b1)
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        show_text(SCREEN_SIZE[0]-200, 15, f'Осталось пуль: {self.amount_bullets}', WHITE, 30)
        for i in range(self.lives):
            x = SCREEN_SIZE[0] - 20 - self.img_live.get_width()
            x -= i * (10 + self.img_live.get_width())
            y = 40
            window.blit(self.img_live, (x,y)) 
window = display.set_mode((SCREEN_SIZE))
display.set_caption('Шутер')
player = Player(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - SPRITE_SIZE - 5, 'rocket.png', 3)

enemies = sprite.Group()
for _ in range(10):
    enemies.add(Enemy(randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, 'ufo.png', 3))

missed_counter = Counter(10, 10, 'Кол-во пропущенных:',20)

killed_count = Counter(10, 35, 'Кол-во подстельнных:', 20)
bg = transform.scale(image.load("galaxy.jpg"),SCREEN_SIZE)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

clock = time.Clock()

game = True
finish = False
while game:
    clock.tick(60)
    for  e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:        
        window.blit(bg, (0, 0))
        player.show()
        player.move()
        missed_counter.show()
        killed_count.show()
        bullets.draw(window)
        bullets.update()
        enemies.update()
        asteroids.update()
        asteroids.draw(window)
        sprites_list = sprite.groupcollide(enemies, bullets, False, True)
        for s in sprites_list:
            s.rect.y = -SPRITE_SIZE
            s.rect.x = randint(0, SCREEN_SIZE[1] - SPRITE_SIZE)
            killed_count.count += 1
            killed_count.render()
        if killed_count.count >= 10:
            finish = True
            show_text(300, 200, 'YOU WIN!', WHITE)
        for s in sprite.spritecollide(player, enemies, False) + sprite.spritecollide(player, asteroids, False):
            s.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            s.rect.y = -SPRITE_SIZE
            player.lives -= 1
            if isinstance(s, Enemy):
                killed_count.count += 1
                killed_count.render()
        if player.lives <= 0:   
            finish = True
            show_text(300, 200, 'YOU LOSE!', WHITE)
        display.update()



       