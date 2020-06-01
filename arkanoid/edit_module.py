import pygame
from time import sleep

from block_module import *
import arkanoid_module as ar

import edit_handler_module as hd
import load_module as ld
import save_module as sv

def draw_grid(size, surface):
    """
    This function draws grid, used in as a visual indication of different sections of the screen, used only in debugging.

    ...

    Parameters
    ----------
    size : (int, int)
        game window size, (width, height)
    surface : pygame.surface
        canvas to draw on
    """

    x = 0
    y = 0

    # draw a horizontal line (where, colour, start position, end position
    for i in range((size[1] - 60) // 16):
        y = y + 16
        pygame.draw.line(surface,(255, 255, 255), (0, y), (size[0], y))

    # draw a vertical line (where, colour, start position, end position)
    for i in range(size[0] // 16):
        x = x + 16
        pygame.draw.line(surface,(255, 255, 255), (x, 0), (x, size[1] - 60))


def redraw_window(surface, font, size, colors, UI, texts, level, new_block, new_value, collide_flag):
    """
    Core function, it is resposnible for drawing the whole game screen

    ...

    Parameters
    ----------
    surface : pygame.surface
        canvas to draw on
    font : pygame.font
        font used to display score and lives
    size : (int, int)
        game window size (widht, height)
    colors : [(int, int, int)]
        list containing tuples that contain RGB values
    UI : [pygame.Rect]
        list containing UI elements
    texts : [str]
        texts to be displayed
    level : [(pygame.Rect, int)]
        created level (block, color/value)
    new_block : pygame.Rect
        new block
    new_value : int
        value of the new_block
    collide_flag : boolean
        True if new block collides with existing ones else False
    """

    surface.fill((0, 0, 0)) # black color
    
    draw_grid(size, surface)
                         
    for element, color in zip(UI[:4], colors):  # blocks to be placed
        pygame.draw.rect(surface, color, element)

    for element, text in zip(UI[4:], texts):    # UI
        pygame.draw.rect(surface, colors[1] , element)
        gobox = text.get_rect(center = (element.centerx, element.centery))
        surface.blit(text, gobox)

    if new_block is not None:
        pygame.draw.rect(surface, (255,0,0) if collide_flag else colors[new_value - 1], new_block) # change block's color to red if collides

    for rect in level:
        pygame.draw.rect(surface, colors[rect[1] - 1], rect[0])

    pygame.display.update()

def convert_to_BlockClass(input, colors):
    """
    This function converts created level to a one that can be played

    ...

    Parameters
    ----------
    input : [pygame.Rect]
        created level - only rects
    colors: [(int, int, int)]
        list containing tuples that contain RGB values

    Returns
    -------
    output : [BlockClass]
        created level - full
    """

    output = []
    for rect in input:
        row = rect[0].y
        collumn = rect[0].x
        value = rect[1]
        output.append(BlockClass(row, collumn, value, colors[value - 1]))
    return output

def edit_main(window, size, level_to_edit = None):

    """
    Main function that keeps everything running

    ...

    Parameters
    ----------
    surface : pygame.display.set_mode()
        existing screen
    game_size : (width, height)
        game size
    level : [pygame.Rect], by default None
        loaded level
    """

    color_dark_blue = (80, 81, 96)
    color_blue = (104, 130, 158)
    color_green = (174, 189, 56)
    color_dark_green = (89, 130, 67)
    colors = [color_dark_blue, color_blue, color_green, color_dark_green]

    click = pygame.mixer.Sound('./sounds/click.wav')

    clock = pygame.time.Clock() # object that controlls time
    font = pygame.font.SysFont('Comic Sans MS', 15)

    x = int(0.01 * size[0]) # distance between blocks

    block_1 = pygame.Rect(x, ((size[1] - 60) + size[1]) // 2 - 15, 62, 30)
    block_2 = pygame.Rect(x + 80, ((size[1] - 60) + size[1]) // 2 - 15, 62, 30)
    block_3 = pygame.Rect(x + 160, ((size[1] - 60) + size[1]) // 2 - 15, 62, 30)
    block_4 = pygame.Rect(x + 240, ((size[1] - 60) + size[1]) // 2 - 15, 62, 30)
    block_load = pygame.Rect(size[0] + x - 80, ((size[1] - 60) + size[1]) // 2 - 15, 62, 30)
    block_play = pygame.Rect(size[0] + x - 160, ((size[1] - 60) + size[1]) // 2 - 15, 62, 30)
    block_save = pygame.Rect(size[0] + x - 240, ((size[1] - 60) + size[1]) // 2 - 15, 62, 30)
    block_remo = pygame.Rect(size[0] + x - 320, ((size[1] - 60) + size[1]) // 2 - 15, 62, 30)

    block_UI = [block_1, block_2, block_3, block_4, block_load, block_play, block_save, block_remo]

    text_play = font.render("Play", True, (255,255,255)) # rendering texts only once
    text_load = font.render("Load", True, (255,255,255))
    text_save = font.render("Save", True, (255,255,255))
    text_remo = font.render("Remove", True, (255,255,255))

    texts = [text_play, text_load, text_save, text_remo]

    created_level = [] if level_to_edit is None else level_to_edit
        
    new_block = None
    new_value = -1

    loop_flag = True
    remove_flag = False
    load_flag = False
    play_flag = False
    save_flag = False

    is_colliding = False

    # main game loop
    while loop_flag:
        dt = clock.tick(240) # max frames per second
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            loop_flag = False
            sleep(0.2)

        if keys[pygame.K_c]:
            new_block = None
            sleep(0.2)

        for event in pygame.event.get():    # player hits 'X'
            if event.type == pygame.QUIT:
                loop_flag = False

        mouse_pos = pygame.mouse.get_pos();

        # add new block
        if new_block is not None and pygame.mouse.get_pressed()[0] and not is_colliding:
            click.play()
            created_level.append((new_block, new_value))
            new_block = None
        
        # remove block
        if remove_flag:
            for added in created_level:
                if added[0].collidepoint(mouse_pos):
                    mouse_buttons = pygame.mouse.get_pressed()
                    if mouse_buttons[0]:
                        click.play()
                        created_level.remove(added)
                        sleep(0.1)

        # load level to edit
        if load_flag:
            loop_flag = False # exit level editor
            ld.load_main(load_flag, window, size)

        # save created level
        if save_flag:
            save_flag = False
            sv.save_main(window, size, created_level)

        # play created level
        if play_flag:
            play_flag = False
            ar.arkanoid_main(window, size, convert_to_BlockClass(created_level, colors))

        # handle UI                
        for i in range(0, len(block_UI)):
            if block_UI[i].collidepoint(mouse_pos):
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:
                    click.play()
                    sleep(0.1)
                    new_block, new_value, remove_flag, load_flag, play_flag, save_flag = hd.edit_handler(i, block_UI)
         
        # ensure that new block's position is correct 
        if new_block is not None:
            is_colliding = hd.can_new_block_be_placed(new_block, created_level)
            new_block.center = mouse_pos
            if new_block.x < 0:             # prevent block from disappearing - left side of screen
                new_block.x = 0 

            if new_block.x > size[0] - 62:  # prevent block from disappearing - right side of screen
                new_block.x = size[0] - 62
                
            if new_block.y < 0:             # prevent block from disappearing - ceiling
                new_block.y = 0
                
            if new_block.y > size[1] - 60 - 32:  # prevent block from disappearing - floor
                new_block.y = size[1] - 60 - 32

        redraw_window(window, font, size, colors, block_UI, texts, created_level, new_block, new_value, is_colliding)

        # internally process pygame event handlers
        # For each frame of your game, you will need to make some sort of 
        # call to the event queue. This ensures your program can
        # internally interact with the rest of the operating system
        pygame.event.pump()

