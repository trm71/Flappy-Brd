#import pygame,sys module
import pygame
import sys
import random


def flow():
    Win.blit(Base,(position,488))
    Win.blit(Base,(position+461,488))


def creation() :
    random_pos = random.choice(Heights)
    bottom = pipe.get_rect(midtop = (600,random_pos))
    top  = pipe.get_rect(midbottom = (600,random_pos-100))
    return bottom , top
    

def motion(poles):
    for pole in poles :
        pole.centerx -= 5
    return poles 

def display(poles):
    for pole in poles :
        if pole.bottom >= 500:
            Win.blit(pipe,pole)
        else:
            invert= pygame.transform.flip(pipe,False,True)
            Win.blit(invert,pole)


def collisions(poles):
    for pole in poles:
        if bird_Rect.colliderect(pole):
            collide_Sound.play(
                )
            return False

    if bird_Rect.top <= -50 or bird_Rect.bottom >= 488 :
        return False

    return True


def bird_rotation(Bird):
    bird_new = pygame.transform.rotozoom(Bird,-move_var*2,1)
    return bird_new

def animation():
    new_bird = Birds_list[Bird_Index]
    new_Rect = new_bird.get_rect(center = (80,bird_Rect.centery))
    return new_bird,new_Rect
 

def score_display(state):
    if state == 'main' :
        score_board = style.render(str(int(Score)), False, (0,0,0)) 
        score_rect = score_board.get_rect(center = (230, 75))
        Win.blit(score_board,score_rect)
    
    if state == 'over' :
        score_board = style.render(f'Score : {(int(Score))}', False, (0,0,0)) 
        score_rect = score_board.get_rect(center = (230, 75))
        Win.blit(score_board,score_rect)

        high_score_board = style.render(f'High Score : {(int(High_Score))}', False, (0,0,0)) 
        high_score_rect = high_score_board.get_rect(center = (230, 460))
        Win.blit(high_score_board,high_score_rect)

def update(Score,High_Score):
    if High_Score < Score :
        High_Score = Score 
    return High_Score 


#initiating the game
pygame.mixer.pre_init(frequency = 44100 , size = 16, channels=1 , buffer = 500 )
pygame.init()

#width and height of screen is setup
pygame.display.set_caption("Flappy Bird ")
Win = pygame.display.set_mode((461,600)) 
clock= pygame.time.Clock()
style = pygame.font.Font('04B_19.ttf',40)


#Gravityp
g= 0.25
move_var = 0
game_active= True

Score = 0 
High_Score = 0 
#importing images and sounds
highway = pygame.image.load('pics/highway.png').convert()
highway = pygame.transform.scale2x(highway)
highway = pygame.transform.scale2x(highway)
highway = pygame.transform.rotate(highway,90)

Base = pygame.image.load('pics/Base.png').convert()
Base = pygame.transform.scale2x(Base)
position = 0

BirdDown = pygame.image.load('pics/bird_down.png').convert_alpha()
BirdUp =pygame.image.load('pics/bird_up.png').convert_alpha()
BirdMid = pygame.image.load('pics/bird_midflap.png').convert_alpha()
Birds_list = [BirdDown , BirdMid , BirdUp]
Bird_Index = 0 
Bird_Surface = Birds_list[Bird_Index]
bird_Rect = Bird_Surface.get_rect(center = (80,300 ))


Flapping = pygame.USEREVENT + 1
pygame.time.set_timer(Flapping,200)

pipe = pygame.image.load('pics/green.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

Heights = [400,300,350,250]

game_over_screen = pygame.image.load('pics/screen.png').convert_alpha()
game_rect = game_over_screen.get_rect(center = (231,300))


Flap_Sound = pygame.mixer.Sound('Everything/sfx_wing.wav')
collide_Sound = pygame.mixer.Sound('Everything/sfx_hit.wav')


while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()  #quit function
            sys.exit()  #quit the game completely

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE:
                move_var = 0
                move_var -= 7
                Flap_Sound.play()

            if event.key == pygame.K_SPACE and game_active == False :
                game_active = True 
                pipe_list.clear()
                bird_Rect.center = (100,300)
                move_var = 0
                Score = 0 

        if event.type == SPAWNPIPE:
            pipe_list.extend(creation())


        if event.type == Flapping :
            if Bird_Index < 2 :
                Bird_Index +=  1
            else :
                Bird_Index = 0
            Bird_Surface,bird_Rect = animation()




      
    #actually display the backgraound road
    Win.blit(highway, (0,0))
    

    if game_active:
        move_var  += g
        bird_Rotation = bird_rotation(Bird_Surface)
        bird_Rect.centery += move_var
        Win.blit(bird_Rotation,bird_Rect)

        game_active = collisions(pipe_list)

        pipe_list = motion(pipe_list)
        display(pipe_list)



        Score += 0.01
        
        score_display('main')

    else :

        Win.blit(game_over_screen , game_rect)

        instruct = style.render(f'Use Spacebar To Play', False, (0,0,0)) 
        instruct_rect = instruct.get_rect(center = (240, 120))
        Win.blit(instruct,instruct_rect)


        High_Score = update(Score,High_Score)
        score_display('over')



     #base
    position += -1
    flow()
    if position <= -600:
        position = 0
    
    
    pygame.display.update()
    clock.tick(120)    #frame update command