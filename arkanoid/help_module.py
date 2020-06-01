import pygame
from time import sleep

def redraw_window(surface, font, size, text, colors, powerups):
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
    text : str
        text to display
    colors : [(int, int, int)]
        list containing tuples that contain RGB values
    powerups : [str]
        list that contains powerups descriptions
    """

    surface.fill((0, 0, 0))       # black color
    x = 20
    y = 20
    height = blit_text(text, (255, 255, 255), font, surface, (x,y)) # where the info text has ended
    tmp = height
    k = 0
    for i in range(0,2): # render powerup symbol and its description, in two collumns
        for j in range(0,6):
            text_surface = font.render(powerups[k], True, (255, 255, 255))
            surface.blit(text_surface, (x, tmp))
            pygame.draw.rect(surface, colors[k], (x + int(0.2*size[0]), tmp, 16, 16))
            tmp += font.get_height() + 10
            k += 1
        x += int(0.3 * size[0])
        tmp = height

    pygame.display.update()

def blit_text(text, color, font, surface, position_start):
    """
    This function crops text to fit it in window. It adds '\n' when len(line) + len(word) > window width. And renders it afterwards

    ...

    Parameters
    ----------
    text : str
        text to be rendered after adding '\n'
    color : (int, int, int)
        text color, RGB value
    font : pygame.font
        text font
    surface : pygame.surface
        canvas to draw on
    position_start : int
        where the text should start

    Returns
    -------
    y : int
        y position of the last line
    """

    words = []

    for word in text.splitlines():
        words.append(word.split(' '))

    space = font.size(' ')[0]     # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = position_start

    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]        # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = position_start[0]     # Reset the x.
        y += word_height          # Start on new row.

    return y

def help_main(window, size):
    """
    Main function that keeps everything running

    ...

    Parameters
    ----------
    surface : pygame.display.set_mode()
        existing screen
    game_size : (width, height)
        game size
    """
    clock = pygame.time.Clock() # object that controlls time
    font = pygame.font.SysFont('Comic Sans MS', int(0.025*size[1]))

    text = "Simple Arkanoid Clone created as a project for the\nWWW and Script Languages classes at AGH University of Science and Technology\nKarol Wnęk ICT studies, second year, may 2020\n\nCONTROLS\n--------------------\nmovement: left and right arrow\nlaunch ball: spacebar\nresume: spacebar\nquicksave: s\nquickload: l\npause: p\nback to the previous screen: escape\ncancel block placing: c\nTo load a level enter its name, press 'enter' and then click on the 'Load' button.\nTo save a level enter its name, press 'enter' and then click on the 'Save' button.\n\nPOWERUPS\n--------------------"

    powerups = ["ball damage x2", "double ball", "triple ball", "APFSDS", "larger player", "smaller player", "faster ball", "slower ball", "extra life", "-1 life", "inverted controls", "random explosion"]

    colors = [(89, 84, 214), (0, 187, 173), (0, 173, 108), (189, 189, 189), (0, 140, 249), (235, 172, 35), (209, 99, 230), (0, 198, 248), (0, 110, 0), (184, 0, 88), (255, 146, 135), (178, 69, 2)]

    loop_flag = True
   
    while loop_flag:
        dt = clock.tick(240) # max frames per second
        keys = pygame.key.get_pressed()

        if  keys[pygame.K_ESCAPE]:
            loop_flag = False
            sleep(0.2)

        for event in pygame.event.get():    # player hits 'X'
            if event.type == pygame.QUIT:
                loop_flag = False

        redraw_window(window, font, size, text, colors, powerups)

        # internally process pygame event handlers
        # For each frame of your game, you will need to make some sort of 
        # call to the event queue. This ensures your program can
        # internally interact with the rest of the operating system
        pygame.event.pump()