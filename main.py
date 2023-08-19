import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tank them Sweetie!")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BORDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 300
ONE_HIT = pygame.USEREVENT + 1
TWO_HIT = pygame.USEREVENT + 2
TANK_WIDTH,TANK_HEIGHT=55,40
HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',120)

TANK_ONE_IMG = pygame.image.load(os.path.join('assets' , 'spaceship_yellow.png'))
TANK_ONE = pygame.transform.rotate(pygame.transform.scale(TANK_ONE_IMG,(TANK_WIDTH,TANK_HEIGHT)),270)

TANK_TWO_IMG = pygame.image.load(os.path.join('assets','spaceship_red.png'))
TANK_TWO = pygame.transform.rotate(pygame.transform.scale(TANK_TWO_IMG,(TANK_WIDTH,TANK_HEIGHT)), 90)

BACKGROUND =pygame.transform.scale(pygame.image.load(os.path.join('assets','space.png')),(WIDTH,HEIGHT))




def draw_window(one,two,one_bullets,two_bullets,one_health,two_health):
    WIN.blit(BACKGROUND,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    one_health_text = HEALTH_FONT.render('Health: '+ str(one_health),1,WHITE)
    two_health_text = HEALTH_FONT.render('Health: '+ str(two_health),1,WHITE)
    WIN.blit(TANK_ONE,(one.x,one.y))
    WIN.blit(one_health_text,(WIDTH - one_health_text.get_width()-10,10))
    WIN.blit(two_health_text,(10,10))
    WIN.blit(TANK_TWO,(two.x,two.y))
    for bullets in one_bullets:
          pygame.draw.rect(WIN,YELLOW,bullets)
    for bullets in two_bullets:
          pygame.draw.rect(WIN,RED,bullets)      
    pygame.display.update()


def one_movement(keys_pressed,one): #RIGHT SIDE  
    if keys_pressed[pygame.K_LEFT] and one.x - VEL - one.width > BORDER.x - 35: #left
            one.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and one.x + VEL < WIDTH - 35: #right
            one.x += VEL
    if keys_pressed[pygame.K_UP] and one.y - VEL > 0: #up
            one.y -= VEL    
    if keys_pressed[pygame.K_DOWN] and one.y + VEL + one.height < HEIGHT - 15: #down
            one.y += VEL

def two_movement(keys_pressed,two): #LEFT SIDE 
    if keys_pressed[pygame.K_a] and two.x - VEL > 0: #left
            two.x -= VEL
    if keys_pressed[pygame.K_d] and two.x + VEL + two.width < BORDER.x: #right
            two.x += VEL
    if keys_pressed[pygame.K_w] and two.y - VEL > 0: #up
            two.y -= VEL    
    if keys_pressed[pygame.K_s] and two.y + VEL + two.height < HEIGHT - 15: #down
            two.y += VEL

def handle_bullets(one_bullets,two_bullets,one,two):
      
      for bullet in one_bullets:
            bullet.x -= BULLET_VEL
            if two.colliderect(bullet):
                  pygame.event.post(pygame.event.Event(TWO_HIT))
                  one_bullets.remove(bullet) 
            elif bullet.x > WIDTH:
                  one_bullets.remove(bullet)      

      for bullet in two_bullets:
            bullet.x += BULLET_VEL
            if one.colliderect(bullet):
                  pygame.event.post(pygame.event.Event(ONE_HIT))
                  two_bullets.remove(bullet)                       
            elif bullet.x < 0:
                  two_bullets.remove(bullet)    

def draw_winner(text):
      draw_text = WINNER_FONT.render(text,1,WHITE)
      WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2 ))
      pygame.display.update()
      pygame.time.delay(5000)

def main():
    one = pygame.Rect(700,300,TANK_WIDTH,TANK_HEIGHT)
    two = pygame.Rect(100,300,TANK_WIDTH,TANK_HEIGHT)
    one_bullets = []
    two_bullets = []
    one_health = 30
    two_health = 30
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:                     

                if event.key == pygame.K_LCTRL and len(two_bullets) < MAX_BULLETS:                                     #LEFT_TWO
                      bullet = pygame.Rect(two.x + two.width,two.y + two.height//2 - 2,10,5) 
                      two_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(one_bullets) < MAX_BULLETS:                                     #RIGHT_ONE
                      bullet = pygame.Rect(one.x,one.y + one.height//2 - 2,10,5) 
                      one_bullets.append(bullet) 
   
            if event.type == ONE_HIT:
                one_health -= 1 

                 
               
            if event.type == TWO_HIT:   
                two_health -= 1
                

              
                
        winner_text = ''         
        if one_health <= 0:
              winner_text = 'hehe, red won!'   
        if two_health <= 0:
              winner_text = 'hehe, yellow won!'
        if winner_text != '':
              draw_winner(winner_text)
              break                                      
        
        keys_pressed = pygame.key.get_pressed()
        one_movement(keys_pressed,one)
        two_movement(keys_pressed,two)
        handle_bullets(one_bullets,two_bullets,one,two)
        draw_window(one,two,one_bullets,two_bullets,one_health,two_health)        



    main()

if __name__ == "__main__":
    main()