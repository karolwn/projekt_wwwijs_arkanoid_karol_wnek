"""
This is a simple Arkanoid clone

arkanoid.py is the main script that keeps everything running (game)
required modules:
    - pygame, developed on version 1.9.6

    - ball_module.py
    - block_module.py
    - player_module.py
    - powerup_module.py
    - powerup_handler_module.py

For more complete game with menus and level editor launch main_menu_module.py

Created as a project for the WWW and Script Languages classes at AGH University of Science and Technology
Karol Wnęk ICT studies, second year, may 2020
"""

import pygame
import random
from math import sqrt
from time import sleep
import pickle

from ball_module import *
from block_module import *
from player_module import *
from powerup_module import *
from powerup_handler_module import *

def redraw_window(surface, blocks, player, balls, font, size, powerups, save, load):
    """
    Core function, it is resposnible for drawing the whole game screen

    ...

    Parameters
    ----------
    surface : pygame.surface
        canvas to draw on
    blocks : [BlockClass]
        list containing remaining blocks
    player : PlayerClass
        player
    balls : [BallClass]
        list containing remaining balls
    font : pygame.font
        font used to display score and lives
    size : (int, int)
        game window size (widht, height)
    powerups : [PowerupClass]
        list that contains all powerups that should be drawn
    save : boolean
        flag used to determine whether "saved" message should be displayed
    load : boolean
        flag used to determine whether quickload error has occoured and error message should be displayed
    """

    surface.fill((0, 0, 0)) # black color

    for ball in balls:
        ball.draw(surface)

    player.draw(surface)

    text_surface = font.render("points: " + str(player.points), True, (0,255,0))
    surface.blit(text_surface, (10, size[1] - 45))

    text_surface = font.render("lives: " + str(player.lives), True, (0,255,0))
    surface.blit(text_surface, (200, size[1] - 45))

    if not player.in_move:
        text_surface = font.render("pause", True, (0,255,0))
        surface.blit(text_surface, (size[0] - 70, size[1] - 45))

    if save:
        text_surface = font.render("saved", True, (0,255,0))
        surface.blit(text_surface, (size[0] - 130, size[1] - 45))

    if load:
        text_surface = font.render("no quicksave to load", True, (0,255,0))
        surface.blit(text_surface, (size[0] - 400, size[1] - 45))

    for block in blocks:    # draw blocks
        block.draw(surface)

    if len(powerups) > 0:   # draw powerups if necessary
        for powerup in powerups:
            powerup.draw(surface)

    pygame.display.update()


# 
def generate_level(rows, collums, colors):
    """
    Generate level by making a list containing blocks

    ...

    Parameters
    ----------
    rows : int 
        how many rows of blocks should be generated
    collumns : int
        how many collumns of blocks should be generated
    colors : [(int, int, int)]
        list containing tuples that contain RGB values

    Returns
    -------
    generated level : [BlockClass]
        list containg created blocks
    """

    layout = []
    for i in range(0,rows, 2):         # blocks are 2 grid's pixels high (32 px)
        for j in range(0,collums, 4):  # blocks are 4 grid's pixels wide (64 px)

            # used in color picking and hp of the block - how many times it's necessary to hit it before dostroying it
            temp_random_value = random.randint(0,3)
            
            #layoutOfBlocks.append(object block(xPos, yPos, hp, (random colour form palette)) 
            layout.append(BlockClass(i * 16, j * 16, temp_random_value + 1, (colors[temp_random_value])))

    return layout

def hit_reg(player, ball, blocks, surface, colors, points_for_hit, hitmarker, bounce, size, dt, powerups):
    """
    Handles hit registration

    ...

    Parameters
    ----------
    player : PlayerClass
        player
    ball : BallClass
        ball
    surface : pygame.surface
        canvas to draw on
    colors : [(int, int, int)]
        list containing tuples that contain RGB values
    poins_for_hit : int
        how many points the player should be awarded with for hitting a block
    hitmarker : pygame.mixer.Sound
        sound to play after hitting block
    bounce : pygame.mixer.Sound
        sound to play after hitting player
    size : (int, int)
        window size (width, height)
    dt : int
        how long it took to render previous frame
    powerups : [PowerupClass]
        list containing all visible powerups

    """

    # ball vs player 
    middle_of_player = ((player.position + player.size) * 16 + (player.position * 16)) // 2
    hitbox = player.get_hitbox()

    if ball.player_hit(hitbox, size[1]): 
        bounce.play()
        if ball.pos_x < middle_of_player - 5: # ball hits left side of the palayer
            speed_modifier = (middle_of_player - ball.pos_x) / 64
            if speed_modifier > 0.7:
                speed_modifier = 0.7
            ball.vel_x = -ball.vel * speed_modifier
            
        elif ball.pos_x > middle_of_player + 5: # ball hits right side of the palayer
            speed_modifier = (ball.pos_x - middle_of_player) / 64
            if speed_modifier > 0.7:
                speed_modifier = 0.7
            ball.vel_x = ball.vel * speed_modifier

        else:
            ball.vel_x = 0 
            ball.vel_y = ball.vel
        ball.vel_y = sqrt((ball.vel**2) - (ball.vel_x**2))

    # ball vs block
    for block in reversed(blocks): # blocks that are positioned at rows closest to the player, are at the end of blocks []
        if (ball.pos_x - block.center[0])**2 + (ball.pos_y - block.center[1])**2 < 8000: # calculation colision for nearest blocks
            if ball.block_hit(block.hitbox, dt):
                hitmarker.play()
                player.points += points_for_hit
                color_index = colors.index(block.color)
                block.value -= ball.power
                block.color = colors[color_index - 1]
                if block.value <= 0:
                    if random.randint(1,2) == 1:
                        powerups.append(PowerupClass(random.randint(1,12), (int(block.center[0]), int(block.center[1]))))
                    blocks.remove(block)
                    player.points += block.point_prize * 100

def reset_balls(player, balls, size_y, ball_speed, ball_power):
    """
    Resets list that contains balls to its default state - only one ball, not moving, located in the middle of the player

    ...

    Parameters
    ----------
    player : PlayerClass
        player
    balls : [BallClass]
        list that needs to be reseted
    size_y : int
        window height
    ball_speed : int
        default ball speed
    ball_power : int
        default ball damage

    Returns
    -------
    balls : [BallClass]
        reseted balls
    """

    balls.clear();
    balls.append(BallClass(player, size_y, ball_speed, ball_power))
    player.invert = 1
    player.speed_mod = 1.0
    return balls

def quick_save(player, balls, blocks, powerups, colors):
    """
    Enables user to perform quicksave
    
    ...

    Parameters
    ----------
    player : PlayerClass
        player
    balls : [BallClass]
        list containing balls
    blocks : [BlockClass]
        list containing blocks
    powerups : [PowerupClass]
        list containing powerups
    colors : [(int, int, int)]
        list containing tuples that contain RGB values
    """

    f = open('quick_save.sav', 'wb')
    pickle.dump([player, balls, blocks, powerups, colors], f)
    f.close()

def quick_load():
    """
    Enables user to perform quickload

    ...

    Returns
    -------
    loaded_data : [PlayerClass, [BallClass], [BlockClass], [PowerupClass], [(int, int, int)]] OR empty list in case of exception

    """

    try:
        f = open('quick_save.sav', 'rb')
        loaded_data = pickle.load(f)
        f.close()
        return loaded_data
    except: 
        return []

def arkanoid_main(surface = None, game_size = None, level = None):
    """
    Main function that keeps everything running

    ...

    Parameters
    ----------
    surface : pygame.display.set_mode(), None by default
        existing screen
    game_size : (width, height), None by default
        game size
    level : [BlockClass], None by default
        loaded level
    """

    # reading config file
    f = open('game.cfg', 'r')
    lines = [f.readline() for x in range(8)]
    f.close()

    size = (int(lines[0].split()[1]), int(lines[1].split()[1]) + 60) if game_size is None else game_size
    player_size = int(lines[2].split()[1])
    ball_speed = (int(lines[3].split()[1]) / 100) * 800 
    ball_speed = 1600 if ball_speed > 1600 else ball_speed
    ball_power = int(lines[4].split()[1])
    points_for_hit = int(lines[5].split()[1])
    number_of_collumns = int(lines[6].split()[1]) * 4
    number_of_rows = int(lines[7].split()[1]) * 2
    

    limit_IO = 0
    save_timer = 0
    load_error_timer = 0
    
    color_dark_blue = (80, 81, 96)
    color_blue = (104, 130, 158)
    color_green = (174, 189, 56)
    color_dark_green = (89, 130, 67)
    colors = [color_dark_blue, color_blue, color_green, color_dark_green]

    moveLimitter = 1 # slows down player's movement

    # sounds
    pygame.mixer.set_num_channels(16)
    oof = pygame.mixer.Sound('./sounds/death.wav')
    hitmarker = pygame.mixer.Sound('./sounds/hitmarker.wav')
    bounce = pygame.mixer.Sound('./sounds/bounce.wav')
    pow = pygame.mixer.Sound('./sounds/powerup.wav')

    window = pygame.display.set_mode(size) if surface is None else surface
    pygame.display.set_caption('arkanoid v1.0')
    clock = pygame.time.Clock() # object that controlls time
    font = pygame.font.SysFont('Comic Sans MS', 20)

    player = PlayerClass(player_size, size)

    use_loaded_level = False

    if level is None:
        blocks = generate_level(number_of_rows, number_of_collumns, colors)
    else:
        blocks = level.copy()
        use_loaded_level = True

    balls = [BallClass(player, size[1], ball_speed, ball_power)]
    powerups = []

    loop_flag = True
    notification_saving = False
    notification_load_error = False
    
    while loop_flag:
        dt = clock.tick(240) # max frames per second
        keys = pygame.key.get_pressed()
        player.move(moveLimitter, keys, size[0], dt)
        if player.move_limitter  > 0:
            player.move_limitter -= 1
        
        # IO operations limitter
        if limit_IO  > 0:
            limit_IO -= 1
        
        # how long to dispay 'saved'
        if save_timer > 0:
            save_timer -= 1
            if save_timer == 0:
                notification_saving = False


        # how long to display 'no quicksave to load'
        if load_error_timer > 0:
            load_error_timer -= 1
            if load_error_timer == 0:
                notification_load_error = False

        if  keys[pygame.K_ESCAPE]:
            loop_flag = False
            sleep(0.2)

        for event in pygame.event.get():    # player hits 'X'
            if event.type == pygame.QUIT:
                loop_flag = False
        
        # pause powerups
        if keys[pygame.K_p]:
            for powerup in powerups:
                powerup.in_move = False
        
        # quicksave
        if keys[pygame.K_s]:
            if limit_IO == 0:
                limit_IO = 200
                quick_save(player,balls,blocks,powerups, colors)
                save_timer = int(dt * 20)
                notification_saving = True

        # quickload
        if keys[pygame.K_l]:
            if limit_IO == 0:
                limit_IO = 200
                loaded = quick_load()
                if len(loaded) > 0:
                    player = loaded[0]
                    balls = loaded[1]
                    blocks = loaded[2]
                    powerups = loaded[3]
                    colors = loaded[4]
                else:
                    notification_load_error = True
                    load_error_timer = int(dt * 20)

        # pause player, pause balls and update their position if new ball, detect lost balls, move balls
        for ball in balls:
            if ball.new_ball:
                ball.pos_update(player)

            if keys[pygame.K_p]:
                ball.in_move = False
                player.in_move = False
                
            if ball.pos_y + ball.radius >= size[1] - 60:
                if len(balls) > 1:
                    balls.remove(ball)
                else:
                    oof.play()
                    reset_balls(player, balls, size[1], ball_speed, ball_power)
                    player.lives -= 1

            ball.movement(keys, size, bounce, dt)

            # checking colisions twice in one frame
            hit_reg(player, ball, blocks, window, colors, points_for_hit, hitmarker, bounce, size, dt, powerups)
            hit_reg(player, ball, blocks, window, colors, points_for_hit, hitmarker, bounce, size, dt, powerups)
        
        powerups, balls, blocks = powerup_handler(powerups, blocks, balls, player, hitmarker, pow, dt, size, ball_speed, ball_power, keys)

        # game over
        if player.lives < 0:
            blocks = level.copy() if use_loaded_level else generate_level(number_of_rows, number_of_collumns, colors)
            balls = reset_balls(player, balls, size[1], ball_speed, ball_power)
            player.points = 0
            player.lives = 3

        # finished level
        if len(blocks) == 0:
            if not use_loaded_level:
                colors.clear()
                ball_speed *= 1.1 if ball_speed < 1600 else 1
                player.speed_mod += 0.1 if player.speed_mod < 2 else 0
                points_for_hit *= 5
                color_dark_blue = (255 - color_dark_blue[0], 255 - color_dark_blue[1], 255 - color_dark_blue[2])
                color_blue = (255 - color_blue[0], 255 - color_blue[1], 255 - color_blue[2])
                color_green = (255 - color_green[0], 255 - color_green[1], 255 - color_green[2])
                color_dark_green = (255 - color_dark_green[0], 255 - color_dark_green[1], 255 - color_dark_green[2])
                colors = [color_dark_blue, color_blue, color_green, color_dark_green]
                blocks = generate_level(number_of_rows, number_of_collumns, colors)
                balls = reset_balls(player, balls, size[1], ball_speed, ball_power)
                player.lives += 3
            else:
                balls = reset_balls(player, balls, size[1], ball_speed, ball_power)
                loop_flag = False

        redraw_window(window, blocks, player, balls, font, size, powerups, notification_saving, notification_load_error)

        # internally process pygame event handlers
        # For each frame of your game, you will need to make some sort of 
        # call to the event queue. This ensures your program can
        # internally interact with the rest of the operating system
        pygame.event.pump()
#------------------------------------------------------------------------------

if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 16, 512)
    pygame.mixer.init()
    pygame.init()
    arkanoid_main()
    pygame.quit()
