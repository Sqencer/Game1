import pygame
import os
import random
pygame.init()

#Set up
WIDTH, HEIGHT = 500, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('HAHAHAHAHA')

#Game constant
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)

FPS = 60
VEL = 5
MAX_BULLET = 5

HIT_TEXT = 'You got hit'
GOT_HIT = pygame.USEREVENT + 1
HITFONT = pygame.font.SysFont('comicsans', 70)

#ONI
oni_width, oni_height = 100, 100
YEEHA = pygame.image.load(os.path.join('projects', 'Game1', 'yata.png'))
ONI = pygame.transform.scale(YEEHA, (oni_width, oni_height))

#blade aura
blade_aura = pygame.image.load(os.path.join('projects', 'Game1', 'bladeaura.png'))
aura_width, aura_height = 60, 60
aura = pygame.transform.scale(blade_aura, (aura_width, aura_height))

#enemy
EMEMY = pygame.image.load(os.path.join('projects', 'Game1', '6w6.png'))

#background
BG = pygame.image.load(os.path.join('projects', 'Game1', 'background.png'))


def draw(player, bullets, enemies, bg):
    for d in bg:
        WINDOW.blit(BG, (d.x, d.y))
    WINDOW.blit(ONI, (player.x, player.y))
    for i in bullets:
        WINDOW.blit(aura, (i.x, i.y))
    for _ in enemies:
        WINDOW.blit(EMEMY, (_[0].x, _[0].y))
    pygame.display.update()

def draw_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    WINDOW.blit(img, (x, y))
    pygame.display.update()

def move(keypressed, player):
    if keypressed[pygame.K_a] and player.x != 0: #LEFT
        player.x -= VEL
    if keypressed[pygame.K_d] and player.x != (WIDTH-oni_width): #Right
        player.x += VEL
    if keypressed[pygame.K_s] and player.y != (HEIGHT-oni_height):#Down
        player.y += VEL
    if keypressed[pygame.K_w] and player.y != 0: #Up
        player.y -= VEL
        
def bulletmove(bullets:list):
    for bullet in bullets:
        bullet.y -= VEL+2
        if bullet.y < 0:
            bullets.remove(bullet)

def enemyspawn(enemies):
    ranx = random.randint(100, 400)
    rany = random.randint(0, 70)
    ranwid = random.randint(30, 80)
    if len(enemies) < 6:
            enemyrect = pygame.Rect(ranx, rany, ranwid, ranwid)
            xvel = random.randint(-3, 3)
            yvel = random.randint(3, 5)
            vel = (xvel, yvel)
            enemies.append((enemyrect, vel))
    for i in enemies:
        i[0].x += i[1][0]
        i[0].y += i[1][1]
        if i[0].y > HEIGHT or i[0].x < 0 or i[0].x >WIDTH :
            enemies.remove(i)

def colide(bullets, enemies , player):
    for enemy in enemies:
        index = enemy[0].collidelist(bullets)
        if index != -1:
            enemies.remove(enemy)
            bullets.pop(index)
        if player.colliderect(enemy[0]):
            enemies.remove(enemy)
            pygame.event.post(pygame.event.Event(GOT_HIT))

def bgmove(bgrects: list):
    for bg in bgrects:
        bg.y += 5
        if bg.y > HEIGHT:
            bgrects.remove(bg)
    if len(bgrects) < 3:
        y = bgrects[len(bgrects) -1].y
        rect = pygame.Rect(0, y - BG.get_height(), BG.get_width(), BG.get_height())
        bgrects.append(rect)

def testmove(bg):
    bg.y+=2

def main():
    player = pygame.Rect(180, 400, oni_width, oni_height)

    bg = [(pygame.Rect(0, 0, BG.get_width(), BG.get_height()))]
    bullets = []
    enemies = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        keypressed = pygame.key.get_pressed()
        enemyspawn(enemies)
        bulletmove(bullets)
        colide(bullets, enemies, player)
        move(keypressed, player)
        bgmove(bg)
        draw(player, bullets, enemies, bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLET:
                    aura = pygame.Rect(player.x, player.y - aura_height , aura_width, aura_height)
                    bullets.append(aura)

            if event.type == GOT_HIT:
                draw_text(HIT_TEXT, HITFONT, RED, 70, 300)
    
    pygame.quit()

if __name__ == "__main__":
    main()