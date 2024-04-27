from pygame import *
from random import *


window = display.set_mode((700, 500))
backround = transform.scale(image.load('galaxy.jpg'), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reser(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


bullets = sprite.Group()

class Rocket(GameSprite):
    def movement(self):
       keys = key.get_pressed()
       if keys[K_a] and self.rect.x >= 0:
           self.rect.x -= self.speed
       if keys[K_d] and self.rect.x <= 645:
           self.rect.x += self.speed
    def fire(self):
        sfaira = bullet("bullet.png", self.rect.x, 455, 5)
        bullets.add(sfaira)
        

class bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()

class UFO(GameSprite):
    def update(self):
        global missed    
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,635)
            self.speed = randint(1,5)
            missed += 1
            
alien = sprite.Group()
rocket = Rocket('rocket.png', 12, 455, 10)
for i in range(10):
    ufo = UFO('ufo.png', randint(0, 650), 0, randint(1, 5))
    alien.add(ufo)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

font.init()
font2 = font.Font(None, 36)
lose = font2.render("too late", True, (255, 0, 0))



clock = time.Clock()
FPS = 60
finish = False
score = 0
missed = 0
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    collide = sprite.groupcollide(alien, bullets, True, True)
    for i in collide:
        score += 1
        ufo = UFO('ufo.png', randint(0, 650), 0, randint(1, 5))
        alien.add(ufo)
        
    window.blit(backround, (0, 0))
    rocket.reser()
    bullets.draw(window)
    alien.draw(window)

    if sprite.spritecollide(rocket, alien, False) or missed >=6:
        window.blit(lose, (200, 200))
        finish = True

    if finish == False:
        bullets.update()
        alien.update()
        rocket.movement()

    text = font2.render("Score: " + str(score), 1, (255, 255, 255))     
    window.blit(text, (10, 20))
    miss = font2.render("Missed: " + str(missed), 1, (255, 255, 255))
    window.blit(miss, (10, 40))
    clock.tick(FPS)
    display.update()