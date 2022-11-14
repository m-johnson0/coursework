#importing all of my libraies i need to have the game run then initializing my functions for pygame
import sys
import math
import pygame

pygame.init()
pygame.key.set_repeat(5,10)

#this set the size of the display and labels the game window
ScreenWidth = 1000
ScreenHeight = 563
display = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Rat Attack!")
clock = pygame.time.Clock()



#this loades the images for the ground and background   
groundImage = pygame.image.load("ground.png").convert_alpha()
Gwidth = groundImage.get_width()
Gheight = groundImage.get_height()

bgroungImages = []
for i in range(1,6):
    bgroungImage = pygame.image.load(f"bgimg-{i}.png").convert_alpha()
    bgimg = pygame.transform.scale(bgroungImage, (900,563))
    bgroungImages.append(bgimg)
bgroundWidth = bgroungImages[0].get_width()

#these functions moves the different layers of the background at different speeds to have a paralax effect

def draw_BackGround(scroll):
    for x in range (5):
        speed = 0.6
        for i in bgroungImages:
            display.blit(i, (x * bgroundWidth - scroll * speed, 0))
            speed += 0.2

def draw_ground(scroll):
    for x in range(20):
        display.blit(groundImage, ((x * Gwidth) - scroll * 2,ScreenHeight - Gheight ))

#creating lists to hold all of the players walking images 

MoveRight = [pygame.image.load('player_right1.png'),pygame.image.load('player_right2.png'),pygame.image.load('player_right3.png'),pygame.image.load('player_right4.png')]
right = False

MoveLeft = [pygame.image.load('player_left1.png'),pygame.image.load('player_left2.png'),pygame.image.load('player_left3.png'),pygame.image.load('player_left4.png')]
left = False

walkframe = 0
#class for defining the player: where on screen they are their image and all the functions needed

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((x,y, 80 , 180))
        self.vel_y = 0        
    def playerwalk(self,walkframe):
        if left == True:
            for n in range (1,4):
            #Ltemp = ((MoveLeft[walkframe//3],(200,300)))
            #Ltemp = pygame.image.load('player_left1.png').convert_alpha()
                #Ltemp = pygame.image.load(f'player_left{n}.png').convert_alpha()
                Ltemp = pygame.image.load('player_left2.png').convert_alpha()
                LeftSprite = pygame.transform.scale(Ltemp, (120,200))
                display.blit(LeftSprite,(200,300))
        elif right == True:
            for i in range (1,4):
            #Rtemp = ((MoveRight[walkframe//3],(200,300)))
            #Rtemp = pygame.image.load('player_right1.png').convert_alpha()
                #Rtemp = pygame.image.load(f'player_right{i}.png').convert_alpha()
                Rtemp = pygame.image.load('player_right2.png').convert_alpha()
                RightSprite = pygame.transform.scale(Rtemp, (120,200))
                display.blit(RightSprite,(200,300))
        else:
            standingtemp = pygame.image.load('player_right1.png').convert_alpha()
            standing = pygame.transform.scale(standingtemp, (120,200))
            display.blit(standing,(200,300 ))
    def jump(self, x ,y):
        self.playerx = x 
        self.playery = y
        
V = 5
m = 1
isjump = False
        
#class for making the bullets and calculating their speed and direction

class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 20
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_velocity = math.cos(self.angle) * self.speed
        self.y_velocity = math.sin(self.angle) * self.speed
    def main(self, display):
        self.x -= int(self.x_velocity)
        self.y -= int(self.y_velocity)
        pygame.draw.circle(display, (20,20,20), (self.x, self.y), 5 )

#Enemy class holding all of the variables and functiosn for the enemies

class Enemy:
    def __init__(self,x,y,health):
        self.x = x
        self.y = y
        self.health = health

    def DrawEnemy(self,display,x,y):
        RatTemp = pygame.image.load('Rat-Enemy.png').convert_alpha()
        resizedrat = pygame.transform.scale(RatTemp,(120,200))
        display.blit(resizedrat,(x,y))

#list for holding all the bullets currently on screen and the scroll varible for moving the background

player_bullets = []

scroll = 0

#getting the input from the player and defining an object from the player class which will be the character

keys = pygame.key.get_pressed()

player1 = Player(200,310)

enemy1 = Enemy(800,210,3)

#main game loop running all of the functions needed to have the game run and refreshing the screen

while True:
    clock.tick(60)
    draw_BackGround(scroll)
    draw_ground(scroll)
    left = False
    right = False
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and scroll > 0:
                left = True
                scroll -= 3
            if event.key == pygame.K_d and scroll < 3000:
                right = True
                scroll += 3
            if event.key == pygame.K_w and player1.y > 310:
                isjump = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullets.append(PlayerBullet(player1.x, player1.y, mouse_x, mouse_y))
                for bullet in player_bullets:
                    bullet.main(display)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    if player1.y <= 310:
        isjump = False

    if isjump == True:
        F=(1/2)*m*(v**2)
        player1.y -= F
        v = v-1
        if v<0:
            m =-1
        if v==-6:
            isjump = False
            v = 5
            m = 1

    player1.playerwalk(walkframe)
    enemy1.DrawEnemy(display,800,210)

    pygame.display.update()
