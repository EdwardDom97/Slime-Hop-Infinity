#this is going to be a second revision of my Python/pygame project SlimeHopInfinity. Which was previously known as Slime Ranger. This was initially
# inspired by a three hour tutorial  on youtube https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=81s by the content creator Clear Code https://www.youtube.com/@ClearCode. 
#I am doing this revision because I have been doing this on and off a little more seriously the past year and I want to take my first project and now make it better.

#comment 1: you can never have too many comments.

#for the previous versions I completed a 'ground' with a wide .png whereas for this version 
#and forward I think I will attempt a tileset design and make a simple ground loop with respective layers.

#I also plan to introduce the multi-state approach I have been using for the past few projects.


#the most current version

#idea I had today 03/31/24 a co-op mode where the players can die and wait to respawn if the others stay alive, and controller support.
#time challenges.
#second, flying enemy,
#dont forget to add shooting mechanic
#add third animation frame for smoother movement.



#I begin by loading the libraries I am going to need for my program to run. 
import pygame
import sys
import random  # Import the random module


# Initialize the pygame library
pygame.init()


# Set the window title
pygame.display.set_caption("Slime Hop Inifinity    Version 0.0.3       03/25/2024          Tristan Dombroski")


# Set up the window dimensions
window_width = 1600
window_height = 900


#the variable which will take the window_width = 1600, window_height = 900 variables and stores them for the next code bit.
window_size = (window_width, window_height)

# Create the window
screen = pygame.display.set_mode(window_size)

#this is going to be the splash art for the main screen
menu_art = pygame.image.load('graphics/newmenu.png')

#like the previous version, for now I am going to use a png for the ingame background
ingame_art = pygame.image.load('graphics/newsky.png')

#adding this image to serve as a game over screen
gameover_art = pygame.image.load('graphics/gameoverdisplay.png')


#BUTTONS

#this will be the first button introduced into the game, previous version relied on pressing the up arrow to start via text-prompt
#here I am going to add in a few more buttons like controls, exit, options, and maybe something like highscores.
#play game button
play_game_button = pygame.image.load('graphics/playbutton.png')
play_game_button_rect = play_game_button.get_rect(topleft=(100, 300))

#adding in a character button to see how it looks
select_character_button = pygame.image.load('graphics/selectcharacterbutton.png')
select_character_button_rect = select_character_button.get_rect(topleft=(100, 400))

#controls button
controls_button = pygame.image.load('graphics/controlsbutton.png')
controls_button_rect = controls_button.get_rect(topleft=(100, 500))

#options button
options_button = pygame.image.load('graphics/optionsbutton.png')
options_button_rect = options_button.get_rect(topleft=(100, 600))

#exit game button
exit_game_button = pygame.image.load('graphics/exitbutton.png')
exit_game_button_rect = exit_game_button.get_rect(topleft=(100, 700))

#here I am adding a menu display to be used inside of the game state to return to the main menu, will also be including a menu button
menu_display = pygame.image.load('graphics/gamemenudisp.png')
menu_display_rect = menu_display.get_rect(center = (window_width/2, window_height/2))

#Menu button from in-game
menu_button = pygame.image.load('graphics/menubutton.png')
menu_button_rect = menu_button.get_rect(center = (window_width/2, window_height/2))
#here is a controlling variable for the menu which will toggle/bind it to the escape key
show_menu_display = False

#tutorial button from main menu
tutorial_display = pygame.image.load('graphics/tutorialdisplay.png')
tutorial_display_rect = tutorial_display.get_rect(center = (window_width/2, window_height/2))
#toggles the tutorial window on/off
show_tutorial_display = False

#END OF BUTTONS




#here I am going to establish a basic font type and introduce a player health and a player score displays
# Define font variables
game_font = pygame.font.SysFont(None, 54)  # Choose the font type and size



#THIS IS THE ENVIRONMENT VARIABLES
# Load the ground tile image to be used in the game environment
ground_tile = pygame.image.load('graphics/ground_tile.png')

# Define the size of each tile (assuming each tile is 32x32 pixels)
tile_size = 64

# Define the dimensions of your tile map (number of rows and columns)
num_rows = 1
num_cols = window_width // tile_size

#END OF ENVIRONMENT


# LOADING GAME SOUNDS

#here I want to load in a few music samples I made on my yamaha and recorded with bandlad
menusong = pygame.mixer.Sound('sounds/string_and_guitar_loop.wav')
menusong.set_volume(0.4)

gamesong = pygame.mixer.Sound('sounds/harploopforshi.wav')
gamesong .set_volume(0.4)

#END OF LOADING GAME SOUNDS



#THIS IS THE PLAYER RELATED VARIABLES
player_image = pygame.image.load('graphics/player/treddo.png')
player_image_rect = player_image.get_rect(center=(50,800))
# Update the player position based on ground position
player_image_rect.bottomleft = (0, window_height - tile_size)

#player sounds
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
# Set the volume of the jump sound to a lower value
jump_sound.set_volume(0.2)  # Adjust the volume as needed (0.0 to 1.0)

#images to use for the player walk animation
player_walk_image_01 = pygame.image.load('graphics/player/rightwalk01.png')
player_walk_image_02 = pygame.image.load('graphics/player/rightwalk02.png')
player_walk_image_03 = pygame.image.load('graphics/player/leftwalk01.png')
player_walk_image_04 = pygame.image.load('graphics/player/leftwalk02.png')
player_jump_image_01 = pygame.image.load('graphics/player/playerjump01.png')
player_jump_image_02 = pygame.image.load('graphics/player/playerjump02.png')


#this will be the image displayed at the top left to represent the player's health
player_healthbar_display = pygame.image.load('graphics/player/playerhealthbardisplay.png')
player_healthbar_display_rect = player_healthbar_display.get_rect(topleft=(50,100))

#this chunk is dedicated to drawing a green rectangle over the player healthbar visual to represent the current health
current_healthbar_width = 32
current_healthbar_height = 100
current_healthbar_color = (20, 220, 85)

current_healthbar_rect = pygame.Rect(player_healthbar_display_rect.x, player_healthbar_display_rect.y + 64, current_healthbar_width, current_healthbar_height)




# Define a timer for animation
animation_timer = 0
animation_delay = 10  # Adjust the delay to control the animation speed

# Define a timer for jumping animation
#jump_animation_timer = 0
#jump_animation_delay = 1  # Adjust the delay to control the animation speed


# Define player speed
player_speed = 5
player_jump_height = 12
player_jumping = False
gravity = 0.8
max_fall_speed = 10
player_score = 0
player_health = 5

#END OF PLAYER VARIABLES





# Constants for game states (pulled from cape castsea The Ruins)

MENU = 'MENU'
CHARACTER = 'CHARACTER'
GAME = 'GAME'
GAMEOVER = 'GAMEOVER'
OPTIONS = 'OPTIONS'



# Variable to track current game state
current_state = MENU  # Start with the menu state





#start of enemy code, this following section was more or less copied from the original and covers the display of a timer and slime collision
#spawner on the right side of the screen where the slimes seemingly appear from.
spawner = pygame.image.load('graphics/portal.png')
spawn_rect = spawner.get_rect(midbottom = (765, 550))
spawn_rect.bottomleft = (1500, window_height - tile_size)


#my earthslime yay my first enemy I made
# Define maximum and current number of enemy earth slimes
current_enemy_earthslimes = 0
max_enemy_earthslimes = 8

#Earth slime enemy which spawns along the ground off right towards off left.
enemy_earthslime = pygame.image.load('graphics/earthslime.png') #loads an image of my slime within the same directory
enemy_earthslime_rect = enemy_earthslime.get_rect(midbottom = (750, 550)) #uses pygames built in rect function to update the enemy variable, grabs a point 'midbottom' and defines it's location on the x,y axis or window
enemy_earthslime_rect.bottomleft = (700, window_height - tile_size)

# Initialize the slime list to have multiple slimes
earthslime_rect_list = []

#here are some varibles I will use to control the enemy earthslimes
enemy_earthslime_speed = 3
current_earthslime_spawn_time = 0


# Define minimum and maximum spawn time for enemy earth slimes
min_spawn_time = 2000  # 2 seconds
max_spawn_time = 11000  # 11 seconds

# Randomly generate the spawn time within the specified range
enemy_earthslime_spawn_time = random.randint(min_spawn_time, max_spawn_time)


enemies_can_spawn = False
#end of enemy code for now




# Main game loop
while True:
    # Handle events outside of the current states so it can be used within all three when called for.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        #this checks for the mouse button being pressed down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button


                #handles the mouse button down events during the MENU state
                if current_state == MENU:

                    #this is the play button's logic in the menu state
                    if play_game_button_rect.collidepoint(event.pos):
                        gamesong.stop()
                        menusong.stop()
                        current_state = GAME

                    #this is the select character button's logic in the menu state
                    if select_character_button_rect.collidepoint(event.pos):
                        gamesong.stop()
                        current_state = CHARACTER

                    #this is the options button's logic in the menu state
                    if options_button_rect.collidepoint(event.pos):
                        current_state = OPTIONS

                    
                    #this is the controls button's logic in the menu state
                    if controls_button_rect.collidepoint(event.pos):
                        show_tutorial_display = not show_tutorial_display
                    
                    #this is the exit button's logic in the menu state
                    if exit_game_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()



                if current_state == CHARACTER:
                    if menu_button_rect.collidepoint(event.pos):
                        #this is where I am trtying to clear the game screen when returning to the menu
                        current_state = MENU


                #handles the mouse button down events during the GAME state
                if current_state == GAME:
                    if menu_button_rect.collidepoint(event.pos):
                        #this is where I am trtying to clear the game screen when returning to the menu
                        current_state = MENU



                if current_state == OPTIONS:
                    if menu_button_rect.collidepoint(event.pos):
                        #this is where I am trtying to clear the game screen when returning to the menu
                        current_state = MENU



                #handles the mouse button down events during the GAMEOVER state
                if current_state == GAMEOVER:

                    if menu_button_rect.collidepoint(event.pos):


                        player_score = 0
                        current_state = MENU



        #this will handle key events like user interface and more.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_state == GAME:
                    show_menu_display = not show_menu_display

         

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()
    # Update player position based on keys being held down
   

    if keys[pygame.K_w] and not player_jumping:
        player_score += 1
        jump_sound.play()
        player_velocity = -player_jump_height
        player_jumping = True


      
    if keys[pygame.K_s]:
        player_image_rect.y += player_speed


    if keys[pygame.K_a]:
        player_image_rect.x -= player_speed

        # Increment animation timer
        animation_timer += 1
        if animation_timer >= animation_delay:
            # Switch between the two walking images
            player_image = player_walk_image_03 if player_image == player_walk_image_04 else player_walk_image_04
            animation_timer = 0  # Reset the timer


    if keys[pygame.K_d]:
        player_image_rect.x += player_speed

        # Increment animation timer
        animation_timer += 1
        if animation_timer >= animation_delay:
            # Switch between the two walking images
            player_image = player_walk_image_01 if player_image == player_walk_image_02 else player_walk_image_02
            animation_timer = 0  # Reset the timer



    # Ensure player stays within the window boundaries
    player_image_rect.x = max(0, min(player_image_rect.x, window_width - player_image_rect.width))
    player_image_rect.y = max(0, min(player_image_rect.y, window_height - player_image_rect.height))




    # Apply gravity
    if player_jumping:
        player_velocity += gravity
        player_velocity = min(player_velocity, max_fall_speed)  # Cap falling speed
        player_image_rect.y += player_velocity

    # Check collision with ground
    if player_image_rect.bottom >= window_height - tile_size:
        player_image_rect.bottom = window_height - tile_size
        player_jumping = False
        player_velocity = 0




   




    #This will be the menu logic state
    if current_state == MENU:


        #This controls the music being played ingame during the menu, character, and options state
        #menusong.play()

        #sets the ingame display menu to false after returning to the menu state from the game state
        show_menu_display = False
       



        # Menu state logic
        pass




    #this will be the character selection logic state
    if current_state == CHARACTER:

        

        #sets the ingame display menu to false after visiting the character state from the menu state
        show_menu_display = False
       



        # Character state logic
        pass




    #this will be the game logic state
    if current_state == GAME:

        show_tutorial_display = False
        # game state logic




        pass




    #this will be the gameover logic state
    if current_state == GAMEOVER:
        # gameover state logic




        pass




    #options logic start
    if current_state == OPTIONS:
       

        # options state logic
        pass

    #options logic end







    #LOGIC ABOVE THIS LINE RENDERING BELOW THIS LINE







    #menu state rendering
    if current_state == MENU:

        #hopefully this line will clear the slimes from the game screen whenever the player transitions to the menu
        current_enemy_earthslimes = 0 

        #removes blitting the slimes on the screen during the menu phase
        #earthslime_rect_list.remove(slime_rect)
        earthslime_rect_list.clear()

        #reset the players position, score, and health in game through the menu
        player_image_rect.bottomleft = (0, window_height - tile_size)



        # Fill the screen with a color (e.g., white) (RED, GREEN, BLUE)
        #(155, 155, 155) GRAY
        #blits the screen art I designed into the mene or as the menu's background
        screen.blit(menu_art, (0, 0))


        #Rendering BUTTONS onto the MENU State
        #play button 
        screen.blit(play_game_button, play_game_button_rect)

        #character button
        screen.blit(select_character_button, select_character_button_rect)
        
        #controls button
        screen.blit(controls_button, controls_button_rect)

        #options button
        screen.blit(options_button, options_button_rect)

        #exit button
        screen.blit(exit_game_button, exit_game_button_rect)

        #End of rendering BUTTONS 





        if show_tutorial_display:
            #earthslime_rect_list.clear()   #clears the screen in prep for the menu state, might keep it this way for awhile because I like it... kinda.
              # Adjust frame rate to pause the game
            screen.blit(tutorial_display, tutorial_display_rect)
            


        


        pass

    #end of menu state rendering



    #options state rendering
    elif current_state == CHARACTER:

        #fills gray
        screen.fill((155, 155, 155))

        #displays the menu button
        screen.blit(menu_button, menu_button_rect)

        pass



    #end of options state rendering




    #game state rendering
    elif current_state == GAME:

        

        #leaving a comment because I had a good idea, I can use score poitns to buy health points or other things like items or abilities or even skills. I would assign a button
        # like increase jump is 20 points and when the player clicks the button it will att to the player_jump_height. I also need to work on a save file and a save system.
        #


        #Check if the maximum number of enemy earth slimes has been reached
        current_earthslime_spawn_time += 100 


        #fills the screen with a blank gray color for now
        screen.fill((155, 155, 155))


        screen.blit(ingame_art, (0, 0))


        #the ground as a loop instead of a wide 1600p image
        # Draw the ground tiles
        for row in range(num_rows):
            for col in range(num_cols):
                # Calculate the position to blit the tile
                tile_x = col * tile_size
                tile_y = window_height - tile_size  # Position the tiles at the bottom of the screen
                # Blit the ground tile at the calculated position
                screen.blit(ground_tile, (tile_x, tile_y))


        # Check collision between player and ground tiles
        for row in range(num_rows):
            for col in range(num_cols):
                # Calculate the position of the ground tile
                tile_x = col * tile_size
                tile_y = window_height - tile_size  # Position the tiles at the bottom of the screen
                
                # Create a rectangle for the ground tile
                ground_tile_rect = pygame.Rect(tile_x, tile_y, tile_size, tile_size)
                
                # Check collision between player and ground tile
                if player_image_rect.colliderect(ground_tile_rect):
                    player_jumping = False
                    # Adjust player's position if there's a collision
                    if player_image_rect.bottom > ground_tile_rect.top:
                        player_image_rect.bottom = ground_tile_rect.top





        #load the player image
        screen.blit(player_image, player_image_rect)


        #load the player healthbar display
        screen.blit(player_healthbar_display, player_healthbar_display_rect)

        # Update the green health bar height based on the player's health
        #current_healthbar_rect.height = player_health * 20

        # Calculate the height of the green health bar based on the player's health
        current_healthbar_rect.height = int((player_health / 5 ) * current_healthbar_height)

        # Calculate the y-position of the health bar based on the remaining health
        current_healthbar_rect.y = player_healthbar_display_rect.y + (current_healthbar_height - current_healthbar_rect.height) + 32


        #here I want to draw a green rectangle over the player healthbar display to serve as an active or current health. providing a visual and textual display
        pygame.draw.rect(screen,  current_healthbar_color,  current_healthbar_rect)




        #this section will be dedicated to spawning slimes in the active game section
        # Logic for continuously spawning new earth slimes
        enemies_can_spawn = True
    

        if enemies_can_spawn:
            
            
            # Logic for continuously spawning new earth slimes
            if current_enemy_earthslimes <= max_enemy_earthslimes:
                if current_earthslime_spawn_time >= enemy_earthslime_spawn_time:
                    new_enemy_earthslime_rect = enemy_earthslime_rect.copy()
                    new_enemy_earthslime_rect.x = window_width  # Spawn at the right edge of the screen
                    earthslime_rect_list.append(new_enemy_earthslime_rect)
                    current_enemy_earthslimes += 1
                    enemy_earthslime_spawn_time = random.randint(min_spawn_time, max_spawn_time)
                    current_earthslime_spawn_time = 0  # Reset the spawn timer
                
                



       # Render all enemy earth slimes
        for slime_rect in earthslime_rect_list:
            screen.blit(enemy_earthslime, slime_rect)


        # Move each slime and check if it goes off-screen
        for slime_rect in earthslime_rect_list:
            slime_rect.x -= enemy_earthslime_speed

            if slime_rect.right <= 0:
                #if the slime wanders of screen it will be removed instead of teleported.
                current_enemy_earthslimes -= 1
                earthslime_rect_list.remove(slime_rect)

                #old
                # Reset position if slime goes off-screen
                #slime_rect.bottomleft = (window_width, window_height - tile_size)

            
            #here I am going to attempt to add in collision detection between the slime and the player.
            # Collision detection between player and enemy earth slime
            if player_image_rect.colliderect(slime_rect):
                player_score -= 1
                player_health -= 1
                current_enemy_earthslimes -= 1
                earthslime_rect_list.remove(slime_rect)




        #here I will attempt to move the earthslime
        enemy_earthslime_rect.x -= enemy_earthslime_speed



        if enemy_earthslime_rect.right <= 0:
            enemy_earthslime_rect.bottomleft = (window_width, window_height - tile_size)
            


        #here I am going to provide the textual displays for the player score and player health
         # Render player score
        player_score_text = game_font.render(f"Score: {player_score}", True, (255, 255, 255))  # Render player score onto a surface
        player_score_text_rect = player_score_text.get_rect(midtop=(window_width // 2, 10))  # Position the text surface
        screen.blit(player_score_text, player_score_text_rect)


        
        #player health text
        player_health_text = game_font.render(f"Health: {player_health}", True, (255, 255, 255))  # Render player score onto a surface
        player_health_text_rect = player_health_text.get_rect(midtop=(window_width // 2, 64))  # Position the text surface
        screen.blit(player_health_text, player_health_text_rect)



        #load the spawner
        screen.blit(spawner, spawn_rect)



        #reveals the menu in the middle of the screen if the escape key is pressed.
        if show_menu_display:
            #earthslime_rect_list.clear()   #clears the screen in prep for the menu state, might keep it this way for awhile because I like it... kinda.
              # Adjust frame rate to pause the game
            screen.blit(menu_display, menu_display_rect)
            screen.blit(menu_button, menu_button_rect)
            
        
            


        #end of game call should be at the bottom
        #if the player health is less than zero it will reset the players score and health adn return the state to the menu for now. after skills and upgrades, well, needs work.
        if player_health <= 0:
            current_enemy_earthslimes = 0
            enemies_can_spawn = False
            #player_score = 0
            #player_health = 5
            current_state= GAMEOVER    #commenting this out because I want to render a gameover screen instead of returning to the menu
            

        if enemies_can_spawn == False:
            earthslime_rect_list.clear()


        #a simple logic loop to keep the player's score at a minimum of zero. it's a little glitchy visually speaking but I will work on that later.
        if player_score <= -1:
            player_score = 0


        pass

    #end of game state rendering




    #start of gameover rendering
    #gameover state rendering
    elif current_state == GAMEOVER:

        #resets the players values health and location
        player_health = 5
        player_image_rect.bottomleft = (0, window_height - tile_size)
        


        #displays the gameover background art
        screen.blit(gameover_art, (0, 0))
        #displays the menu button on the gameover screen
        screen.blit(menu_button, menu_button_rect)

        



         #here I am going to provide the textual displays for the player score and player health
         # Render player score
        player_score_text = game_font.render(f"Final Score: {player_score}", True, (255, 255, 255))  # Render player score onto a surface
        player_score_text_rect = player_score_text.get_rect(midtop=(window_width // 2, 300))  # Position the text surface
        screen.blit(player_score_text, player_score_text_rect)





        pass

    #end of game over rendering




    #options state rendering
    elif current_state == OPTIONS:

        #fills gray
        screen.fill((155, 155, 155))

        #displays the menu buttons for now
        screen.blit(menu_button, menu_button_rect)

        pass


    #end of options state rendering


    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    pygame.time.Clock().tick(60)