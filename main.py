from time import *
from pygame import *
from random import randint

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (700,500))

lost = 0
font.init()
font1 = font.Font(None, 36)
kill = 0
life_count = 5
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, speed_player, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed_player = speed_player
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed_player
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(50,win_width - 50)
            lost = lost + 1
            mixer.music.load('zvuk.ogg')
            mixer.music.play()



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed_player
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed_player
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed_player
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed_player

    def fire(self):

        bullet1 = Bullet('bullet.png', self.rect.centerx - 20 , self.rect.top,  15, 40, 40)
        bullet.add(bullet1)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed_player

        if self.rect.y <0:
            print(1)
            self.kill()


asteroid = Enemy('asteroid.png', 30,randint(0, 600),3,20,139)
asteroid2 = Enemy('asteroid.png', 30,randint(0, 600),3,20,139)
asteroid3 = Enemy('asteroid.png', 30,randint(0, 600),3,20,139)
bon=Player('rocket.png', 300, 400, 8, 100, 100)
enemy = Enemy('ufo.png', 30, 100, 1, 80, 80)
enemy1 = Enemy('ufo.png', 30, 100, 2, 80, 80)
enemy2 = Enemy('ufo.png', 30, 100, 5, 80, 80)
enemy3 = Enemy('ufo.png', 30, 100, 7, 80, 80)
enemy4 = Enemy('ufo.png', 30, 100, 4, 80, 80)





asteroids = sprite.Group()
monsters = sprite.Group()
bullet = sprite.Group()

monsters.add(enemy, enemy3, enemy1, enemy2, enemy4)
asteroids.add(asteroid2, asteroid3,asteroid)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()


run = True

clock = time.Clock()
FPS = 60
finish = False

font2 = font.Font(None, 70)
win = font2.render('You win', True, (255, 215, 0))
lose = font2.render('You lose', True, (255, 0, 0))
font3 = font.Font(None,70)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                mixer.music.load('fire.ogg')
                mixer.music.play()
                bon.fire()

    if finish != True:
        window.blit(background, (0, 0))
        bon.update()
        bon.reset()
        monsters.draw(window)
        monsters.update()
        bullet.draw(window)
        bullet.update()
        asteroids.draw(window)
        asteroids.update()
        sprire_list = sprite.groupcollide(monsters,bullet, True, True)
        for i in sprire_list:
            kill += 1
            enemy = Enemy('ufo.png', randint(50,600), 0, randint(1,7), 80, 80)
            monsters.add(enemy)
        spit_list = sprite.groupcollide(asteroids,bullet, True, True)
        for i in spit_list:
            kill +=   1
            asteroid = Enemy('ufo.png', randint(50, 600), 0, randint(1, 7), 80, 80)
            asteroids.add(asteroid)
        jizny = font3.render('Жизни' + str(life_count), 1, (125,125,125))
        jizny_spis = sprite.spritecollide(bon, monsters, True)
        for i in jizny_spis:
            life_count-=1
            if life_count == 0:
                finish = True
                life_count -= 1
                window.blit(lose, (175,200))


        if lost>20:
            finish = True
            window.blit(lose, (175,200))

        elif kill>20:
            finiish = True
            window.blit(background,(0,0))
            window.blit(win, (175, 200))
            run = False






    text_lose = font1.render('Пропущено' + str(lost), 1, (255,255,255))
    text_kill = font1.render('Счетчик' + str(kill), 1, (255, 255, 255))
    window.blit(text_lose, (0,0))
    window.blit(jizny, (0, 450))
    window.blit(text_kill, (0, 27))
    display.update()
    clock.tick(FPS)
sleep(2)