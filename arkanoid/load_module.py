import pygame
from time import sleep

from block_module import *
import arkanoid_module as ar
import edit_module as ed

def redraw_window(surface, font, size, texts, colors, rects, is_not_ready):
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
    texts : [str]
        texts to be displayed
    colors : [(int, int, int)]
        list containing tuples that contain RGB values
    rects : [pygame.Rect]
        list containing UI elements
    is_not_ready : boolean
        flag used to determine whether user has entered level's name
    """

    surface.fill((0, 0, 0))       # black color

    for rect, text in zip(rects, texts):

        #change color for unclickable button
        pygame.draw.rect(surface, colors[0], rect) if text == texts[-1] and is_not_ready else pygame.draw.rect(surface, colors[1], rect)
        gobox = text.get_rect(center=(rect.centerx, rect.centery))
        surface.blit(text, gobox)

    pygame.display.update()


def load_main(edit, window, size):

    """
    Main function that keeps everything running

    ...

    Parameters
    ----------
    edit : boolean
        tells whether it should load level for playing or editing
    surface : pygame.display.set_mode()
        existing screen
    game_size : (width, height)
        game size
    """

    color_dark_blue = (80, 81, 96)
    color_blue = (104, 130, 158)
    color_green = (174, 189, 56)
    color_dark_green = (89, 130, 67)
    colors = [color_dark_blue, color_blue, color_green, color_dark_green]

    click = pygame.mixer.Sound('./sounds/click.wav')

    clock = pygame.time.Clock() # object that controlls time
    font = pygame.font.SysFont('Comic Sans MS', int(0.025*size[1]))
    text_info = font.render("Enter the name of the desired level below", True, (255,255,255))
    text_done = font.render("Load", True, (255,255,255))
    user_input = ""

    enter_level_rect = pygame.Rect(int(size[0] / 2 - 0.3 * size[0]), int(size[1] / 2 - 0.05 * size[1] - 0.15 * size[1]), int(0.6 * size[0]), int(0.1 * size[1]))
    text_input = pygame.Rect(int(size[0] / 2 - 0.3 * size[0]), int(size[1] / 2 - 0.05 * size[1]), int(0.6 * size[0]), int(0.1 * size[1]))
    done_button = pygame.Rect(int(size[0] / 2 - 0.1 * size[0]), int(size[1] / 2 - 0.05 * size[1] + 0.15 * size[1]), int(0.2 * size[0]), int(0.1 * size[1]))
    rects = [enter_level_rect, text_input, done_button]
    texts = [text_info, user_input, text_done]

    loop_flag = True
    input_loop = False
    is_not_ready = True
   
    while loop_flag:
        dt = clock.tick(240) # max frames per second
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            loop_flag = False
            sleep(0.2)

        for event in pygame.event.get():    # player hits 'X'
            if event.type == pygame.QUIT:
                loop_flag = False

        mouse_pos = pygame.mouse.get_pos()
        
        if text_input.collidepoint(mouse_pos):  # collision input box - player
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:    # mouse left button
                click.play()
                sleep(0.1)
                input_loop = True

        while input_loop:

            # Returns a single event from the queue. If the event queue is empty an event of type pygame.
            # NOEVENT will be returned immediately. The returned event is removed from the queue
            event = pygame.event.poll()
            
            keys = pygame.key.get_pressed()
    
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)  # returns string id of pressed key.
        
                if len(key) == 1:                 # this covers all letters and numbers not on numpad.
                    user_input += key

                elif key == "backspace":
                    user_input = user_input[:len(user_input) - 1]

                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:  # finished typing.
                    input_loop = False
                    is_not_ready = False
                    sleep(0.2) # prevent registering pressed keys multiple times
        
                texts[1] = font.render(user_input, True, (255,255,255))                 # update user input - string
                redraw_window(window, font, size, texts, colors, rects, is_not_ready)   # update screen

        texts[1] = font.render(user_input, True, (255,255,255))
        redraw_window(window, font, size, texts, colors, rects, is_not_ready)

        if done_button.collidepoint(mouse_pos) and not is_not_ready:    # perform loading
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                click.play()
                sleep(0.1)

                try:
                    f = open('./levels/' + user_input + '.lvl', 'r')
                    lines = f.readlines()
                    level = []
                    for line in lines:
                        tmp = line.split()
                        if edit:
                            level.append((pygame.Rect(int(tmp[1]), int(tmp[0]), 62, 30), int(tmp[2]))) # load for editing
                        else:
                            level.append(BlockClass(int(tmp[0]), int(tmp[1]), int(tmp[2]), colors[int(tmp[2]) - 1])) # load for playing
                    
                    f.close()
                    loop_flag = False
                    
                    if edit:
                        ed.edit_main(window, size, level)       # launch level editor
                    else:
                        ar.arkanoid_main(window, size, level)   # launchh game

                except IOError:
                   texts[0] = font.render("wrong level name, please try again", True, (255,255,255))
                   is_not_ready = True

        # internally process pygame event handlers
        # For each frame of your game, you will need to make some sort of 
        # call to the event queue. This ensures your program can
        # internally interact with the rest of the operating system
        pygame.event.pump()
