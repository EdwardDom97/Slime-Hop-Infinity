import pygame, sys #always import pygame
from pygame.locals import * #imports local files for smoother coding, idk
from random import randint #this imports the random library and allows for random choices




def display_score(): #this is my first decalred class that has it's own code to draw and track the players active game score
                        #I can create as many as I want and I can even learn to store the results on a high score page
    current_time = int(pygame.time.get_ticks() /1000) - start_time #turns millisecconds into seconds
    score_surf = test_font.render(f'Score: {current_time}', False,(217,103,79))
    score_rect = score_surf.get_rect(center = (75, 200))
    screen.blit(score_surf, score_rect)


def slime_movement(slime_list): #this class allows the movement of the slimes I loaded with images and gave rectangles
    if slime_list:              
        for slime_rect in slime_list:
            slime_rect.x -= 3
            screen.blit(enemy, slime_rect) #draws the images onto the screen that I already decalred. enemy = pygame.image.load('graphics/earthslime.png')
            
                    

        slime_list = [slime for slime in slime_list if slime.x > -100] #this is the variable that is being updated with the class's commands and has an attacthed function to 'respawn' the slimes by 
        
            
        return slime_list
    
    else: return []

def collisions(player, slimes): #here is my collision class im not exactly sure I have this right either but checks to see if the rects in the player and the slimes are touching i think it's off because I dont see a variable named slimes just enemy
    if slimes: 
        for slime_rect in slimes:
            if player.colliderect(slime_rect): return False
    return True
                                  
#I have the start the whole process with the init statement
pygame.init() #that's it

#now I can set up my screen
menu = pygame.image.load('graphics/menu.png')

test_font = pygame.font.SysFont('calibri', 50)                           #loads python's default text
#this is where I set up my pygame window and define all my surfaces: (score, health, time, ect)
screen = pygame.display.set_mode((800, 600)) #boom window
pygame.display.set_caption('Slime Hop Inifinity. Version 0.0.2                              Tristan Dombroski') #this is still version 0.1 because I don't have an .exe yet
clock = pygame.time.Clock() #creates time or the measurement of frames, doesn't have to be called clock

#create an if game active state
game_active = False #start off with false for the menu
start_time = 0 #this set's the player's score to zero



#my earthslime yay my first enemy I made
#Obstacles

enemy = pygame.image.load('graphics/earthslime.png') #loads an image of my slime within the same directory
enemy_rect = enemy.get_rect(midbottom = (750, 550)) #uses pygames built in rect function to update the enemy variable, grabs a point 'midbottom' and defines it's location on the x,y axis or window

slime_rect_list = [] #this creates an empty list that I coded a class for 


#my spawner I made for slimes because I cannot figure out random movement yet

spawner = pygame.image.load('graphics/portal.png')
spawn_rect = spawner.get_rect(midbottom = (765, 550))

#my player image and rectangle

player = pygame.image.load('graphics/treddo.png')
player_rect = player.get_rect(midbottom = (25, 550)) #creates a surface and draws a rectangle around it and i can specify where to grab the image

#environment

sky = pygame.image.load('graphics/sky.png')
ground = pygame.image.load('graphics/ground.png')
jump_sound = pygame.mixer.Sound('sounds/freesound/jump.wav')

#slime_spawn = pygame.mixer.Sound('sounds/freesound/spawn.wav')

startb = pygame.image.load('graphics/start_button.png')
startb_rect = startb.get_rect(midbottom = (200, 375))
escb = pygame.image.load('graphics/esc_button.png')
escb_rect = escb.get_rect(midbottom = (200, 425))

#my music and sounds mostly come from Alex McCulloch whom I find to be amazing from OpenGame Art
theme = pygame.mixer.music.load('sounds/Alex_McCulloch/amss.wav')
theme = pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


#some way or the other .display.flip() draws everything to the surface
pygame.display.flip()

#after loading images and sprites I have to define additional variables like movement
#or gravity, items, interactions and collisions, this was a part I was missing on my own
#without pre-defining variables here, I cannot run effective code in my active game loop
Right = False
Left = False #by creating these variables and setting them to false when I call them in my game loop on a key event I can set it to true and change my position
enemy_left = False
enemy_right = False

#physics for player
player_loc = [0, 450]
player_grav = 0 #this is a crude way to start the process of adding physics


#timer for slime spawn time
slime_timer = pygame.USEREVENT + 1
pygame.time.set_timer(slime_timer, 1100)
#print(slime_timer)


#I am to believe the code I am about to use below represents the or a main event
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        screen.blit(menu, (0, 0))
        screen.blit(startb, startb_rect)
        screen.blit(escb, escb_rect)
        
        
        if event.type == KEYDOWN:
              if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
        if game_active:
            if event.type == KEYDOWN: #checks to see if a button is pressed
                if event.key == K_RIGHT: #what button is specifically looked for
                    Right = True #what happens with the variable above game loop
                if event.key == K_LEFT:
                    Left = True
                if event.key == K_UP and player_rect.bottom >= 550:
                    jump_sound.play()
                    player_grav = - 10
              
                if event.key == K_SPACE:
                    game_active = False
               

            if event.type == KEYUP: #checks to see if any buttons are released
                if event.key == K_RIGHT:#again what button is exactly looked for
                    Right = False #resets the vraible to its origial values
                if event.key == K_LEFT:
                    Left = False
           
        else:
            if event.type == KEYDOWN and event.key == K_UP:   #THIS IS THE SECTION THAT CHECKS TO SEE IF THE UP ARROW WAS PRESSED TO RESET THE GAME, I NEED TO ADD START BUTTON AND MOUSE CODES TO DETECT                                                              
                game_active = True
                Right = False
                Left = False
                enemy_rect.left = 750
                player_rect.right = 50
                start_time = int(pygame.time.get_ticks() / 1000) - start_time  #sets the score/timer to 0
            

        if event.type == slime_timer and game_active:          #controls slime location, change later #im seeing append again
            slime_rect_list.append(enemy.get_rect(midbottom = (randint(750, 1200),550)))
                #slime_spawn.play(loops = 1)  I cannot figure out an appropiate way to time the slime spawn noise
            print('test')
     
           

                
        
    if game_active:    

      
    
        
        #player    
        player_grav += 0.5
        player_rect.y += player_grav
        if player_rect.bottom >= 550: player_rect.bottom = 550
        if player_rect.x <=0 : player_rect.x = 0
        if player_rect.x >= 770 : player_rect.x = 770
        
        screen.blit(sky, (0, 0)) #I am redrawing my screen inside the active game loop
        screen.blit(ground, (0, 550))
        screen.blit(player, player_rect) #this draws my character in the game loop
        #screen.blit(startb, startb_rect)

        #Obstacle/slime movement
        slime_rect_list = slime_movement(slime_rect_list) #this variable is equal to my class and what it does plus this variable
        


        #collision
        game_active = collisions(player_rect, slime_rect_list) #this is saying if the game is active it wants to update and look for the collisions class between the player_rect and slime_rect_list every frame


        screen.blit(spawner, spawn_rect) #this could be moved
        display_score() #this uses pygame to display the score I defined as a variable earlier
    

        
        #screen.blit(sky, (0,0))
        if Right == True: #an if statement that uses my moving variables and uses my below key events that alter the true and false states of moving does not necessarily have to implemented this way or named this.
            player_rect[0] += 4 #this is where the actual movement is happening
        if Left == True:
            player_rect[0] -= 4



        # I want my slime code to go here to either make him move left and right or jump.
        #ignore the above comment and possibly this one
                                      
            
        #my score
        

        #trying to play sound when slimes touch the spawner
        #if enemy_rect.colliderect(spawn_rect):
        #    pygame.mixer.Sound
            
            

        
        #checking to see if my slime is touching my hero... he better not.
        #This is where I also want to change the game_active state to not end until collision has occured
        #three times, or add a health bar system
        if player_rect.colliderect(enemy_rect): #checks to see if the player_rect and the enemy rect collide
            game_active = False
            Right = False
            Left = False#updates the game_active variable with a boolean true or false, in this case now false
            start_time = 0 #resets the player's score

            
    else: #this being the end of my code updates everything and resets everything like the menu and clearing all the
        #lists that were created during the active game session
        #screen.blit(menu, (0,0))   #THIS RIGHT HERE DRAWS A NEW MENU AFTER A LOST GAME I LEFT A COMMENT BECAUSE I DRAW A MENU UP TOP BUT MIGHT CHANGE THINGS
        slime_rect_list.clear() #clears the list I created and defined earlier
        start_time = 0 #resets the score
    

    
        
    pygame.display.update()
    clock.tick(60)#updates the screen every frame within the active game loop
    
            



pygame.display.update() #updates the window itself whenever there are other specified commands

