##import sys
##sys.path.append("c:\users\22gaom\appdata\roaming\python\python36\site-packages")

import pygame as p
import os
from random import randint

def setup():
    global clock,screen,font_title,font_stats,running,option_list
    global paused,game_finished,hs_saved
    global stars,bullets,ship_png,ship,powerups
    global enemies,enemy_bullets
    global current_level,level_completed,level_text
    global stats_game,stats_ship
    running = True

    p.font.init()
    font_title = p.font.SysFont("Lucida Console",24)
    font_stats = p.font.SysFont("Times New Roman",25)
    
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
    p.init()
    screen = p.display.set_mode((1000,680))
    p.display.set_caption("weird game thing")
    clock = p.time.Clock()
    
    ship_png = p.transform.scale(p.image.load('ship.png'),(75,75))
    ship = Ship(0,500)
    bullets = []
    powerups = []
    stars = []
    option_list = ['off','red','normal']
    enemies = []
    enemy_bullets = []
    current_level = 1
    level_completed = True
    level_text = 0
    
    game_finished = False
    paused = False
    hs_saved = False
    
    #             0     1       2       3 4         5 6 7 8             9
    #             pos   lives   score   hp values   powerup variables   lives
    stats_ship = [0,    0,      0,      0,0,        0,0,0,0,            0]
    #             0       1       2           3           4       5
    #             kills   deaths  dmg dealt   dmg taken   shots   level
    stats_game = [0,      0,      0,          0,          0,      0]
    
    try:
        open("highscores.txt","r")
    except IOError:
        open("highscores.txt","w")

class Star(object):
    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.s = speed
    def draw(self):
        p.draw.circle(screen,p.Color('white'),(self.x,self.y),1)
    def move(self):
        self.y += 5*self.s
        if self.y > 610:
            self.y -= 620
            self.x = randint(0,1000)
            self.s = randint(1,5)
class Ship(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.s = 5
        self.max_hp = 1000
        self.hp = 1000
        self.hitbox = p.Rect(self.x,self.y+17,75,58)
        self.lives = 5
        self.score = 0
        self.score_ = 0
        self.dmg = 10
        self.bullet_speed = 10
        self.cannons = 1
        self.dead = -1
        self.can_move = True
        self.can_shoot = True
    def draw(self):
        if self.dead == -1:
            self.hitbox = p.Rect(self.x,self.y+17,75,58)
            screen.blit(ship_png,(self.x,self.y))
            for enemy in enemies:
                if self.hitbox.colliderect(enemy.hitbox):
                    self.hp -= enemy.dmg
                    enemy.hp -= self.dmg
                    stats_game[2] += self.dmg
                    stats_game[3] += enemy.dmg
                    ship.score += 1000*enemy.type + enemy.dmg
            if self.hp <= 0:
                self.new_life()
        else:
            self.dead += 1
            if self.dead == 100:
                self.dead = -1
                self.can_shoot = True
                self.can_move = True
    def shoot(self):
        if self.cannons == 1:
            bullets.append(Bullet(self.x+35,self.y,self.bullet_speed,self.dmg))
            stats_game[4] += 1
        elif self.cannons == 2:
            bullets.append(Bullet(self.x+25,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+45,self.y,self.bullet_speed,self.dmg))
            stats_game[4] += 2
        elif self.cannons == 3:
            bullets.append(Bullet(self.x+0,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+35,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+70,self.y,self.bullet_speed,self.dmg))
            stats_game[4] += 3
        elif self.cannons == 4:
            bullets.append(Bullet(self.x+0,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+25,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+45,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+70,self.y,self.bullet_speed,self.dmg))
            stats_game[4] += 4
        elif self.cannons == 5:
            bullets.append(Bullet(self.x+0,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+25,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+35,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+45,self.y,self.bullet_speed,self.dmg))
            bullets.append(Bullet(self.x+70,self.y,self.bullet_speed,self.dmg))
            stats_game[4] += 5
    def new_life(self):
        self.lives -= 1
        self.max_hp = max(self.max_hp - 5*current_level, 1000)
        self.hp = max(self.max_hp - 20*current_level, 1000)
        self.s = max(self.s - 2, 5)
        self.dmg = max(self.dmg - 5*current_level, 10)
        self.bullet_speed = max(self.bullet_speed - 5, 10)
        self.score -= 100000
        self.cannons = max(self.cannons - 2, 1)
        self.dead = 0
        stats_game[1] += 1
        if self.lives == 0:
            game_over()
        self.hitbox = p.Rect(0,0,0,0)
        self.can_shoot = False
        self.can_move = False
class Bullet(object):
    def __init__(self,x,y,speed,dmg):
        self.x = x
        self.y = y+35
        self.s = speed
        self.dmg = dmg
        self.hitbox = p.Rect(self.x,self.y,5,15)
    def draw(self):
        p.draw.rect(screen,p.Color(option_list[1]),self.hitbox)
        self.hitbox = p.Rect(self.x,self.y,5,15)
    def move(self):
        self.y -= self.s
        if self.y <= -15:
            bullets.remove(self)
        for enemy in enemies:
            if self.hitbox.colliderect(enemy.hitbox):
                enemy.hp -= self.dmg
                bullets.remove(self)
                ship.score += 1000*enemy.type + enemy.dmg
                stats_game[2] += self.dmg
class Enemy(object):
    def __init__(self,x,y,hp,dmg,chance_to_shoot,move_pattern,t):
        self.x = x
        self.y = y
        self.orig_y = y
        self.hp = hp
        self.dmg = dmg
        self.move_pattern = move_pattern
        self.chance = chance_to_shoot
        self.frame = 0
        self.type = t
        self.entered = False
        self.hitbox = p.Rect(self.x,self.y,75,58)
        
        if self.type == 1: self.img = p.transform.scale(p.image.load('enemy1.png'),(75,75))
        elif self.type == 2: self.img = p.transform.scale(p.image.load('enemy2.png'),(75,75))
        elif self.type == 3: self.img = p.transform.scale(p.image.load('enemy3.png'),(75,75))
        elif self.type == 4: self.img = p.transform.scale(p.image.load('enemy4.png'),(75,75))
        elif self.type == 5: self.img = p.transform.scale(p.image.load('enemy5.png'),(75,75))
        elif self.type == 6: self.img = p.transform.scale(p.image.load('enemy6.png'),(75,75))
        elif self.type == 7: self.img = p.transform.scale(p.image.load('enemy7.png'),(75,75))
        elif self.type == 8: self.img = p.transform.scale(p.image.load('enemy8.png'),(75,75))
        elif self.type == 9: self.img = p.transform.scale(p.image.load('enemy9.png'),(75,75))
        elif self.type == 10: self.img = p.transform.scale(p.image.load('enemy10.png'),(75,75))
    def draw(self):
        screen.blit(self.img,(self.x,self.y))
        self.hitbox = p.Rect(self.x,self.y,75,58)
    def move(self):
        if self.hp <= 0:
            stats_game[0] += 1
            if randint(1,4) == 1:
                powerups.append(Powerup(self.x+35-22,self.y+65-25,randint(0,6)))
            enemies.remove(self)
        if self.entered == False:
            self.y += 5
            if self.y-self.orig_y >= 500:
                self.entered = True
        elif self.entered == True:
            if self.move_pattern == 1:
                pass
            elif self.move_pattern == 2:
                if self.frame >= 1 and self.frame <= 20: self.y += 5/2
                elif self.frame >= 21 and self.frame <= 40: self.x += 5/2
                elif self.frame >= 41 and self.frame <= 60: self.y -= 5/2
                elif self.frame >= 61 and self.frame <= 80: self.x -= 5/2
                if self.frame == 80: self.frame = 0
            elif self.move_pattern == 3:
                if self.frame >= 1 and self.frame <= 40: self.x += 5/4
                elif self.frame >= 61 and self.frame <= 100: self.x -= 5/4
                if self.frame == 120: self.frame = 0
            self.frame += 1
            if randint(1,self.chance) == 1:
                self.shoot()
    def shoot(self):
        enemy_bullets.append(EnemyBullet(self.x,self.y,self.dmg))
class EnemyBullet(object):
    def __init__(self,x,y,dmg):
        self.x = x+35
        self.y = y+65
        self.s = 5
        self.dmg = dmg
        self.hitbox = p.Rect(self.x,self.y,5,15)
    def draw(self):
        p.draw.rect(screen,p.Color('purple'),p.Rect(self.x,self.y,5,15))
        self.hitbox = p.Rect(self.x,self.y,5,15)
    def move(self):
        self.y += self.s
        if self.y >= 615:
            enemy_bullets.remove(self)
        if self.hitbox.colliderect(ship.hitbox):
            ship.hp -= self.dmg
            enemy_bullets.remove(self)
            stats_game[3] += self.dmg
class Powerup(object):
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.s = 5
        
        if type == 2 and ship.s == 10: type = 9
        elif type == 3 and ship.bullet_speed == 20: type = 9
        elif type == 5 and ship.lives == 5: type = 9
        elif type == 6 and ship.cannons == 5: type = 9
        if type == 9:
            if randint(0,1) == 0: type = 0
            else: type = 4
            
        if type == 0:
            self.type = 'hp'
            self.img = p.image.load('hp_up.png')
        elif type == 1:
            self.type = 'max hp'
            self.img = p.image.load('hp_max_up.png')
        elif type == 2:
            self.type = 'speed'
            self.img = p.image.load('spd_up.png')
        elif type == 3:
            self.type = 'bullet speed'
            self.img = p.image.load('bullet_spd_up.png')
        elif type == 4:
            self.type = 'dmg'
            self.img = p.image.load('bullet_dmg_up.png')
        elif type == 5:
            self.type = 'life'
            self.img = p.image.load('life_up.png')
        elif type == 6:
            self.type = 'cannon'
            self.img = p.image.load('cannon_up.png')
    def draw(self):
        screen.blit(self.img,(self.x,self.y))
        self.hitbox = p.Rect(self.x,self.y,50,50)
    def move(self):
        self.y += 3
        if self.y >= 610: powerups.remove(self)
        if self.hitbox.colliderect(ship.hitbox):
            if self.type == 'hp':
                if ship.max_hp-ship.hp >= 10*current_level:
                    ship.hp += 10*current_level
                elif ship.max_hp-ship.hp < 10*current_level:
                    ship.hp = ship.max_hp
            elif self.type == 'max hp':
                ship.max_hp += 5*current_level
            elif self.type == 'speed':
                if ship.s != 10:
                    ship.s += 1
            elif self.type == 'bullet speed':
                if ship.bullet_speed != 20:
                    ship.bullet_speed += 1
            elif self.type == 'dmg':
                ship.dmg += 5
            elif self.type == 'life':
                ship.lives += 1
                if ship.lives > 5:
                    ship.lives = 5
            elif self.type == 'cannon':
                ship.cannons += 1
                if ship.cannons > 5:
                    ship.cannons = 5
            ship.score += 100
            powerups.remove(self)

def text(string,x,y,col):
    text = font_title.render(string,True,p.Color(col))
    widthCenter = x-text.get_rect().width/2
    textHeight = text.get_rect().height
    screen.blit(text,(widthCenter,y-textHeight/2))
def text_stats(string,x,y,col):
    text = font_stats.render(string,True,p.Color(col))
    widthCenter = x-text.get_rect().width/2
    textHeight = text.get_rect().height
    screen.blit(text,(widthCenter,y-textHeight/2))
def draw():
    screen.fill(p.Color(0,0,25))
    for star in stars:
        star.draw()
        star.move()
    for bullet in bullets:
        bullet.draw()
        bullet.move()
    ship.draw()
    for enemy in enemies:
        enemy.draw()
        enemy.move()
    for enemy_bullet in enemy_bullets:
        enemy_bullet.draw()
        enemy_bullet.move()
    for powerup in powerups:
        powerup.draw()
        powerup.move()
def draw_stats():
    global level_text
    if level_text >= 0 and level_text <= 100:
        ship.can_shoot = False
        text("stage "+str(current_level),500,100,'white')
    elif level_text == 101:
        ship.can_shoot = True
    p.draw.rect(screen,p.Color('gray50'),p.Rect(0,600,1000,80))
    text_stats("stage",50,625,'white')
    text_stats(str(current_level),50,655,'white')
    p.draw.rect(screen,p.Color('gray25'),p.Rect(100,600,10,80))
    for i in range(ship.lives):
        screen.blit(p.transform.scale(p.image.load('ship.png'),(50,50)),
                    (55*i+115,615))
    p.draw.rect(screen,p.Color('gray25'),p.Rect(395,600,10,80))
    screen.blit(p.transform.scale(p.image.load('heart.png'),(40,40)),
                (420,635))
    p.draw.rect(screen,p.Color('black'),p.Rect(475,635,510,40))
    p.draw.rect(screen,p.Color('red'),p.Rect(480,640,ship.hp/ship.max_hp*500,30))
    text_stats(str(ship.hp)+"/"+str(ship.max_hp),730,655,'white')
    text_stats("score: " + str(ship.score),730,620,'white')

def menu():
    choice = None
    while choice == None:
        screen.fill(p.Color('black'))
        
        text("space invaders ripoff",500,100,'white')
        
        buttons = [p.Rect(175,200,300,70),
                   p.Rect(525,200,300,70),
                   p.Rect(175,320,300,70),
                   p.Rect(525,320,300,70),
                   p.Rect(175,440,300,70),
                   p.Rect(525,440,300,70)]
        p.draw.rect(screen,p.Color('gray50'),buttons[0])
        text("new game",325,235,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[1])
        text("resume saved game",675,235,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[2])
        text("how to play",325,355,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[3])
        text("view highscores",675,355,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[4])
        text("options",325,475,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[5])
        text("quit",675,475,'white')
        
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                choice = -1
                exit()
            if e.type == p.QUIT:
                choice = -1
                exit()
            if e.type == p.MOUSEBUTTONDOWN:
                for i in range(6):
                    if buttons[i].collidepoint(e.pos):
                        choice = i
        p.display.flip()
        clock.tick(60)
        
    if choice == 0: pass
    elif choice == 1: continue_save()
    elif choice == 2: rules()
    elif choice == 3: highscore()
    elif choice == 4: options()
    elif choice == 5: exit()
def options():
    global stars,paused
    choice = None
    while choice == None:
        screen.fill(p.Color('black'))
        
        text("options",500,100,'white')
        
        buttons = [p.Rect(175,200,300,70),
                   p.Rect(525,200,300,70),
                   p.Rect(175,320,300,70),
                   p.Rect(525,320,300,70),]
        p.draw.rect(screen,p.Color('gray50'),buttons[0])
        text("stars:" + str(option_list[0]),325,235,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[1])
        text("bullet color:" + str(option_list[1]),675,235,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[2])
        text("speed:" + str(option_list[2]),325,355,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[3])
        text("ok",675,355,'white')
        
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                choice = 3
            if e.type == p.QUIT:
                choice = -1
                exit()
            if e.type == p.MOUSEBUTTONDOWN:
                for i in range(4):
                    if buttons[i].collidepoint(e.pos):
                        choice = i
        p.display.flip()
        clock.tick(60)
        
    if choice == 0:
        if option_list[0] == 'on':
            stars = []
            option_list[0] = 'off'
        elif option_list[0] == 'off':
            stars = []
            for i in range(100):
                stars.append(Star(randint(0,1000),randint(0,600),randint(1,5)))
            option_list[0] = 'on'
        options()
    elif choice == 1:
        if option_list[1] == 'red': option_list[1] = 'white'
        elif option_list[1] == 'white': option_list[1] = 'green'
        elif option_list[1] == 'green': option_list[1] = 'blue'
        elif option_list[1] == 'blue': option_list[1] = 'red'
        options()
    elif choice == 2:
        if option_list[2] == 'normal': option_list[2] = 'fast'
        elif option_list[2] == 'fast': option_list[2] = 'normal'
        options()
    elif choice == 3:
        if paused == False: menu()
        elif paused == True: pause()
def rules():
    global paused
    choice = None
    while choice == None:
        screen.fill(p.Color('black'))
        
        text("how to play",500,100,'white')
        
        text("===controls===",500,200,'white')
        text("to move: [W] up [S] down [A] left [D] right   OR   [arrow keys]",
             500,230,'white')
        text("[ESC] quit   [P] pause game   [SPACEBAR] shoot",
             500,260,'white')
        text("===gameplay===",500,300,'white')
        text("shoot enemy ships and try not to get blown up",500,330,'white')
        text("===scoring===",500,370,'white')
        text("losing a life: -100,000",500,400,'white')
        text("enemy kill: +1,000 (per tier) +1 (per unit of damage)",500,430,'white')
        text("boss kill: +100,000 (per tier) +100 (per unit of damage)",500,460,'white')
        text("stage completion: +10,000 (times the stages completed, per stage)",500,490,'white')
        text("collecting a powerup: +100 each",500,520,'white')
        
        buttons = [p.Rect(350,550,300,70)]
        p.draw.rect(screen,p.Color('gray50'),buttons[0])
        text("ok",500,585,'white')
        
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                choice = 0
            if e.type == p.QUIT:
                choice = -1
                exit()
            if e.type == p.MOUSEBUTTONDOWN:
                if buttons[0].collidepoint(e.pos):
                    choice = 0
        p.display.flip()
        clock.tick(60)
        
    if paused == False: menu()
    elif paused == True: pause()
def pause():
    global paused
    choice = None
    while choice == None:
        screen.fill(p.Color('black'))
        
        text("game paused",500,100,'white')
        
        buttons = [p.Rect(175,200,300,70),
                   p.Rect(525,200,300,70),
                   p.Rect(175,320,300,70),
                   p.Rect(525,320,300,70),
                   p.Rect(175,440,300,70),
                   p.Rect(525,440,300,70)]
        p.draw.rect(screen,p.Color('gray50'),buttons[0])
        text("resume game",325,235,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[1])
        text("options",675,235,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[2])
        text("how to play",325,355,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[3])
        text("view game stats",675,355,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[4])
        text("save and quit",325,475,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[5])
        text("quit",675,475,'white')
        
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                choice = 0
            if e.type == p.KEYDOWN and e.key == p.K_p:
                choice = 0
            if e.type == p.QUIT:
                choice = -1
                exit()
            if e.type == p.MOUSEBUTTONDOWN:
                for i in range(6):
                    if buttons[i].collidepoint(e.pos):
                        choice = i
        p.display.flip()
        clock.tick(60)
        
    if choice == 0: paused = False
    elif choice == 1: options()
    elif choice == 2: rules()
    elif choice == 3: game_stats()
    elif choice == 4: save_game()
    elif choice == 5: game_over()
def game_stats():
    global paused,game_finished
    choice = None
    while choice == None:
        screen.fill(p.Color('black'))
        
        text("game statistics",500,100,'white')
        
        text("enemies killed: "+str(stats_game[0]),500,200,'white')
        text("deaths: "+str(stats_game[1]),500,250,'white')
        text("damage dealt: "+str(stats_game[2]),500,300,'white')
        text("damage taken: "+str(stats_game[3]),500,350,'white')
        text("bullets fired: "+str(stats_game[4]),500,400,'white')
        text("score: "+str(ship.score),500,450,'white')
        
        buttons = [p.Rect(350,550,300,70)]
        p.draw.rect(screen,p.Color('gray50'),buttons[0])
        text("ok",500,585,'white')
        
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                choice = 0
            if e.type == p.QUIT:
                choice = -1
                exit()
            if e.type == p.MOUSEBUTTONDOWN:
                if buttons[0].collidepoint(e.pos):
                    choice = 0
        p.display.flip()
        clock.tick(60)

    if game_finished == True: game_over()
    elif paused == True: pause()
def highscore():
    global game_finished
    choice = None
    f = open("highscores.txt","r")
    lines = f.readlines()
    while choice == None:
        screen.fill(p.Color('black'))
        
        text("highscores",500,100,'white')
        
        for i in range(10):
            name = lines[i].split("\t")[1]
            text(str(i+1)+". " + name.replace("\n",""),250,150+40*i,'white')
            text(lines[i].split("\t")[0],750,150+40*i,'white')
        
        buttons = [p.Rect(350,550,300,70)]
        p.draw.rect(screen,p.Color('gray50'),buttons[0])
        text("ok",500,585,'white')
        
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                choice = 0
            if e.type == p.QUIT:
                choice = -1
                exit()
            if e.type == p.MOUSEBUTTONDOWN:
                if buttons[0].collidepoint(e.pos):
                    choice = 0
        p.display.flip()
        clock.tick(60)
    if game_finished == True: game_over()
    elif game_finished == False: menu()

def continue_save():
    global stats_ship,stats_game,current_level
    try:
        f = open("save.txt","r")
        lines = f.readlines()
        for i in range(6):
            stats_game[i] = int(lines[i])
        current_level = stats_game[5]
        for i in range(10):
            stats_ship[i] = int(lines[i+6])
        ship.x = stats_ship[0]
        ship.y = stats_ship[1]
        ship.score = stats_ship[2]
        ship.hp = stats_ship[3]
        ship.max_hp = stats_ship[4]
        ship.s = stats_ship[5]
        ship.bullet_speed = stats_ship[6]
        ship.dmg = stats_ship[7]
        ship.cannons = stats_ship[8]
        ship.lives = stats_ship[9]
        ship.score -= 10000*(current_level-1)
        f.close()
    except IOError:
        f = open("save.txt","w")
        f.close()
def save_game():
    global stats_ship,stats_game
    f = open("save.txt","w")
    stats_game[5] = current_level
    for i in range(6):
        f.write(str(stats_game[i]) + "\n")
    stats_ship[0] = ship.x
    stats_ship[1] = ship.y
    stats_ship[2] = ship.score_
    stats_ship[3] = ship.hp
    stats_ship[4] = ship.max_hp
    stats_ship[5] = ship.s
    stats_ship[6] = ship.bullet_speed
    stats_ship[7] = ship.dmg
    stats_ship[8] = ship.cannons
    stats_ship[9] = ship.lives
    for i in range(10):
        f.write(str(stats_ship[i]) + "\n")
    f.close()
    exit()
def save_highscore():
    f = open("highscores.txt","r")
    lines = f.readlines()
    name = input("Enter your name (must be 20 char or less):  ")
    while len(list(name)) > 20:
        print("This name is too long")
        name = input("Enter your name (must be 20 char or less):  ")
    lines.append(str(ship.score) + "\t" + name +"\n")
    for i in range(len(lines)):
        for j in range(len(lines)-1-i):
            if int(lines[j].split("\t")[0]) < int(lines[j+1].split("\t")[0]):
                temp = lines[j]
                lines[j] = lines[j+1]
                lines[j+1] = temp
    f = open("highscores.txt","w")
    for i in range(10):
        f.write(lines[i])
    f.close()
    print("your name and score are saved")
    print("you can now return to the game window")
    highscore()
def game_over():
    global game_finished,hs_saved
    game_finished = True
    
    if hs_saved == False:
        hs_saved = True
        f = open("highscores.txt","r")
        lines = f.readlines()
        new_hs = False
        for l in lines:
            if int(l.split("\t")[0]) < ship.score:
                new_hs = True
        f.close()
        if new_hs == True:
            choice = None
            while choice == None:
                screen.fill(p.Color('black'))
                
                text("game over",500,100,'white')
                text("you survived "+str(current_level-1)+" levels",500,150,'white')
                text("your score: "+str(ship.score),500,200,'white')
                text("new highscore!",500,300,'white')
                text("after clicking [ok],",500,400,'white')
                text("please proceed to the eclipse console",500,450,'white')
                text("enter your name to save your score",500,500,'white')
                
                buttons = [p.Rect(350,550,300,70)]
                p.draw.rect(screen,p.Color('gray50'),buttons[0])
                text("ok",500,585,'white')
                
                for e in p.event.get():
                    if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                        choice = 0
                    if e.type == p.QUIT:
                        choice = -1
                        exit()
                    if e.type == p.MOUSEBUTTONDOWN:
                        if buttons[0].collidepoint(e.pos):
                            choice = 0
                p.display.flip()
                clock.tick(60)
            save_highscore()
        
    choice = None
    while choice == None:
        screen.fill(p.Color('black'))
        
        text("game over",500,100,'white')
        text("you survived "+str(current_level-1)+" levels",500,150,'white')
        text("your score: "+str(ship.score),500,200,'white')
        
        buttons = [p.Rect(175,320,300,70),
                   p.Rect(525,320,300,70),
                   p.Rect(175,440,300,70),
                   p.Rect(525,440,300,70)]
        p.draw.rect(screen,p.Color('gray50'),buttons[0])
        text("back to main menu",325,355,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[1])
        text("view highscores",675,355,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[2])
        text("view game stats",325,475,'white')
        p.draw.rect(screen,p.Color('gray50'),buttons[3])
        text("quit",675,475,'white')
        
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                choice = 0
            if e.type == p.KEYDOWN and e.key == p.K_p:
                choice = 0
            if e.type == p.QUIT:
                choice = -1
                exit()
            if e.type == p.MOUSEBUTTONDOWN:
                for i in range(4):
                    if buttons[i].collidepoint(e.pos):
                        choice = i
        p.display.flip()
        clock.tick(60)
        
    if choice == 0: main()
    elif choice == 1: highscore()
    elif choice == 2: game_stats()
    elif choice == 3: exit()

def main():
    global screen,ship,running,paused
    global level_completed,current_level,level_text
    setup()
    menu()
    
    while running:
        
        if level_completed == True:
            make_enemies(current_level)
            ship.score += 10000*(current_level-1)
            level_completed = False
        
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                running = False
            if e.type == p.QUIT:
                running = False
            if e.type == p.KEYDOWN and e.key == p.K_SPACE:
                if ship.can_shoot == True:
                    ship.shoot()
            if e.type == p.KEYDOWN and e.key == p.K_p:
                paused = True
                pause()
        
        pressed = p.key.get_pressed()
        if pressed[p.K_d]  and ship.can_move or pressed[p.K_RIGHT] and ship.can_move: ship.x += ship.s
        if pressed[p.K_a]  and ship.can_move or pressed[p.K_LEFT] and ship.can_move: ship.x -= ship.s
        if pressed[p.K_w]  and ship.can_move or pressed[p.K_UP] and ship.can_move: ship.y -= ship.s
        if pressed[p.K_s]  and ship.can_move or pressed[p.K_DOWN] and ship.can_move: ship.y += ship.s
#         if pressed[p.K_SPACE]: ship.shoot()
        
        if ship.x >= 925: ship.x = 925
        elif ship.x <= 0: ship.x = 0
        if ship.y >= 525: ship.y = 525
        elif ship.y <= 0: ship.y = 0   
        
        draw()
        draw_stats()
        
        if len(enemies) == 0:
            level_completed = True
            current_level += 1
            level_text = 0
            ship.score_ = ship.score
        level_text += 1
        
        if option_list[2] == 'normal': fps = 60
        elif option_list[2] == 'fast': fps = 90
        p.display.flip()
        clock.tick(fps)

def make_enemies(lvl):
    if lvl == 1 or lvl == 2 or lvl == 3:
        for x in range(5):
            for y in range(lvl):
                enemies.append(Enemy(x*200+20,y*100+20-500,1,1,200,1,1))
    elif lvl == 4 or lvl == 5 or lvl == 6:
        for x in range(5):
            for y in range(lvl-3):
                enemies.append(Enemy(x*200+20,y*100+20-500,10,10,200,1,1))
    elif lvl == 7 or lvl == 8 or lvl == 9:
        for x in range(5):
            for y in range(lvl-6):
                enemies.append(Enemy(x*200+20,y*100+20-500,20,20,200,1,1))
    elif lvl == 10 or lvl == 11 or lvl == 12:
        for x in range(5):
            for y in range(lvl-9):
                enemies.append(Enemy(x*200+20,y*100+20-500,10,10,200,2,1))
    elif lvl >= 13 and lvl <= 16:
        for x in range(10):
            for y in range(lvl-12):
                enemies.append(Enemy(x*100+20,y*100+20-500,10,10,200,1,1))
    elif lvl >= 17 and lvl <= 20:
        for x in range(10):
            for y in range(lvl-16):
                enemies.append(Enemy(x*100+20,y*100+20-500,20,10,100,1,1))
    elif lvl >= 20 and lvl <= 23:
        for x in range(10):
            for y in range(lvl-19):
                enemies.append(Enemy(x*100+20,y*100+20-500,30,30,100,1,2))
    elif lvl >= 24 and lvl <= 27:
        for x in range(10):
            for y in range(lvl-23):
                enemies.append(Enemy(x*100+20,y*100+20-500,40,40,100,1,2))
    elif lvl >= 28 and lvl <= 30:
        for x in range(10):
            for y in range(lvl-27):
                enemies.append(Enemy(x*100+20,y*100+20-500,50,50,50,1,2))
    elif lvl >= 31 and lvl <= 40:
        for x in range(10):
            for y in range(2):
                enemies.append(Enemy(x*100+20,y*100+20-500,10*lvl,5*lvl,50,1,3))
    elif lvl >= 41 and lvl <= 50:
        for x in range(9):
            for y in range(2):
                enemies.append(Enemy(x*100+20,y*100+20-500,10+10*lvl,10+5*lvl,50,2,4))
    elif lvl >= 51 and lvl <= 60:
        for x in range(9):
            for y in range(2):
                enemies.append(Enemy(x*100+20,y*100+20-500,20+10*lvl,20+5*lvl,50,2,5))
    elif lvl >= 61 and lvl <= 70:
        for x in range(9):
            for y in range(2):
                enemies.append(Enemy(x*100+20,y*100+20-500,30+10*lvl,30+5*lvl,50,2,6))
    elif lvl >= 71 and lvl <= 80:
        for x in range(9):
            for y in range(2):
                enemies.append(Enemy(x*100+20,y*100+20-500,40+10*lvl,40+5*lvl,50,2,7))
    elif lvl >= 81 and lvl <= 90:
        for x in range(9):
            for y in range(2):
                enemies.append(Enemy(x*100+20,y*100+20-500,50+10*lvl,50+5*lvl,50,2,8))
    elif lvl >= 91 and lvl <= 100:
        for x in range(9):
            for y in range(2):
                enemies.append(Enemy(x*100+20,y*100+20-500,60+10*lvl,60+5*lvl,50,2,9))    
    elif lvl >= 101 and lvl <= 199:
        for x in range(9):
            enemies.append(Enemy(x*100+20,0*100+20-500,100+20*lvl,100+10*lvl,50,lvl%2+2,9))
        for x in range(8):
            enemies.append(Enemy(x*100+20+50,1*100+20-500,100+20*lvl,100+10*lvl,50,lvl%2+2,9))
    elif lvl >= 200 and lvl <= 299:
        for x in range(9):
            enemies.append(Enemy(x*100+20,0*100+20-500,100+30*lvl,100+20*lvl,50,lvl%2+2,9))
        for x in range(8):
            enemies.append(Enemy(x*100+20+50,1*100+20-500,100+30*lvl,100+20*lvl,50,lvl%2+2,9))
    elif lvl >= 300 and lvl <= 399:
        for x in range(9):
            enemies.append(Enemy(x*100+20,0*100+20-500,100+40*lvl,100+30*lvl,50,lvl%2+2,9))
        for x in range(8):
            enemies.append(Enemy(x*100+20+50,1*100+20-500,100+40*lvl,100+30*lvl,50,lvl%2+2,9))
    elif lvl >= 400 and lvl <= 499:
        for x in range(9):
            enemies.append(Enemy(x*100+20,0*100+20-500,100+50*lvl,100+40*lvl,50,lvl%2+2,9))
        for x in range(8):
            enemies.append(Enemy(x*100+20+50,1*100+20-500,100+50*lvl,100+40*lvl,50,lvl%2+2,9))
    elif lvl >= 500:
        for x in range(9):
            enemies.append(Enemy(x*100+20,0*100+20-500,100*lvl,100*lvl,50,lvl%2+2,9))
        for x in range(8):
            enemies.append(Enemy(x*100+20+50,1*100+20-500,100*lvl,100*lvl,50,lvl%2+2,9))

main()
