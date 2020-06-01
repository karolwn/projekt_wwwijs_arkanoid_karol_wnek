"""
This is a simple Arkanoid clone

main_menu_module.py is the one script to rule them all. It can launch game, level editor or help
required modules:
    - pygame, developed on version 1.9.6
    - arkanoid_module.py
        ~ ball_module.py
        ~ block_module.py
        ~ player_module.py
        ~ powerup_module.py
        ~ powerup_handler_module.py
    - edit.py
        ~ block_module.py
        ~ load_module.py
        ~ save_module.py
        ~ edit_handler_module.py
    - load.py
        ~ block_module.py
        ~ arkanoid_module.py
        ~ edit_module.py
    - help_module.py

For more simple game (without level editor, menus and help) launch arkanoid.py

Created as a project for the WWW and Script Languages classes at AGH University of Science and Technology
Karol Wnęk ICT studies, second year, may 2020
"""

import pygame
from time import sleep

import arkanoid_module as ar
import load_module as ld
import help_module as hl
import edit_module as ed

def redraw_window(surface, font, size, colors, UI, texts):
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
    texts : [pygame.font.render]
        list containing rendered texts
    """

    surface.fill((0, 0, 0)) # black color
    for element, text in zip(UI, texts):
        pygame.draw.rect(surface, colors[1], element)
        gobox = text.get_rect(center=(element.centerx, element.centery))
        surface.blit(text, gobox)

    pygame.display.update()

def main():
    """
    Main function that keeps everything running

    """

    # reading config file
    f = open('game.cfg', 'r')
    lines = f.readlines()
    size = (int(lines[0].split()[1]), int(lines[1].split()[1]) + 60)
    f.close()
    
    color_dark_blue = (80, 81, 96)
    color_blue = (104, 130, 158)
    color_green = (174, 189, 56)
    color_dark_green = (89, 130, 67)
    colors = [color_dark_blue, color_blue, color_green, color_dark_green]

    # sounds
    pygame.mixer.set_num_channels(16)
    click = pygame.mixer.Sound('./sounds/click.wav')

    window = pygame.display.set_mode(size)
    pygame.display.set_caption('arkanoid v1.0')
    clock = pygame.time.Clock() # object that controlls time
    font = pygame.font.SysFont('Comic Sans MS', int(0.055*size[1]))

    text_play = font.render("Play", True, (255,255,255)) # rendering texts only once
    text_load = font.render("Load", True, (255,255,255))
    text_edit = font.render("Edit", True, (255,255,255))
    text_help = font.render("Help", True, (255,255,255))
    texts = [text_play, text_load, text_edit, text_help]

    # creating rectangles - UI elemnets
    play = pygame.Rect(int(size[0] / 2 - 0.2 * size[0]), int(size[1] / 2 - 0.05 * size[1] - 0.15 * size[1]), int(0.4 * size[0]), int(0.1 * size[1]))
    load = pygame.Rect(int(size[0] / 2 - 0.2 * size[0]), int(size[1] / 2 - 0.05 * size[1]), int(0.4 * size[0]), int(0.1 * size[1]))
    edit = pygame.Rect(int(size[0] / 2 - 0.2 * size[0]), int(size[1] / 2 - 0.05 * size[1] + 0.15 * size[1]), int(0.4 * size[0]), int(0.1 * size[1]))
    about = pygame.Rect(int(size[0] / 2 - 0.2 * size[0]), int(size[1] / 2 - 0.05 * size[1] + 0.3 * size[1]), int(0.4 * size[0]), int(0.1 * size[1]))
    UI_elements =[play, load, edit, about]

    loop_flag = True
   
    while loop_flag:
        dt = clock.tick(240) # max frames per second
        keys = pygame.key.get_pressed()

        if  keys[pygame.K_ESCAPE]:
            loop_flag = False

        for event in pygame.event.get():    # player hits 'X'
            if event.type == pygame.QUIT:
                loop_flag = False

        mouse_pos = pygame.mouse.get_pos()
        
        for i in range(0, len(UI_elements)):
            if UI_elements[i].collidepoint(mouse_pos):
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:
                    click.play()
                    sleep(0.1)
                    if i == 0: # game
                        ar.arkanoid_main(window, size)

                    if i == 1: # load created level         
                        ld.load_main(False, window, size)

                    if i == 2: # level editor
                        ed.edit_main(window, size)

                    if i == 3: # help
                        hl.help_main(window, size)


        redraw_window(window, font, size, colors, UI_elements, texts)

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
    main()
    pygame.quit()