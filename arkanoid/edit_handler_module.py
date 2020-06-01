from pygame import Rect

def edit_handler(pressed_button, UI):
    """
    This function handles presed buttons

    ...

    Parameters
    ----------
    pressed_button : int
        Rectagle responsible for a specific action - pressed by the user, UI index
    UI : [pygame.Rect]
        User Interface

    Returns
    -------
    new_block : pygame.Rect
        new block
    pressed_button : int
        Rectagle responsible for a specific action - pressed by the user, UI index
    remove_flag : boolean
        flag responsible for removing blocks True if remove else False
    load_flag : boolean
        True if user wants to load level else False
    play_flag : boolean
        True if user wants to play the crated level else False
    save_flag : boolean
        True if save level else false
    """

    if pressed_button == 0: # block, value 1
        new_block = UI[pressed_button].copy()
        return new_block, pressed_button + 1, False, False, False, False

    elif pressed_button == 1: # block, value 2         
        new_block = UI[pressed_button].copy()
        return new_block, pressed_button + 1, False, False, False, False

    elif pressed_button == 2: # block, value 3
        new_block = UI[pressed_button].copy()
        return new_block, pressed_button + 1, False, False, False, False

    elif pressed_button == 3: # block, value 4
        new_block = UI[pressed_button].copy()
        return new_block, pressed_button + 1, False, False, False, False

    elif pressed_button == 4: # play
        return None, pressed_button + 1, False, False, True, False                      

    elif pressed_button == 5: # load
        return None, pressed_button + 1, False, True, False, False

    elif pressed_button == 6: # save
        return None, pressed_button + 1, False, False, False, True

    elif pressed_button == 7: # remove
        return None, pressed_button + 1, True, False, False, False

def can_new_block_be_placed(new_block, created_level):
    """
    This function decides whether a new block can be placed (no overlapping with existing ones)

    ...

    Parameters
    ----------
    new_block : pygame.Rect
        new block to be placed
    created_level : [pygame.Rect]
        list containing already existing blocks

    Returns
    -------
    boolean : True if can be placed else False
    """

    # [x[0] for x in created_level] -> unpack tuple and create list from the first elements
    collide_result = new_block.collidelist([x[0] for x in created_level]);
    return True if collide_result > -1 else False