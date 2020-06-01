import pygame

class BlockClass:
    """ 
    A class to represent single block 
    
    ...

    Atributes
    ---------
    row : int
        row in which upper left corner of block is located
    collumn : int
        collumn in which upper left corner of block is located
    value : int
        after how many hits this block should disappear
    point_prize : int
        how many points for destroying block
    color : (int, int, int)
        RGB value representing block's color
    hitbox : (int, int, int, int)
        tuple holding informatiion about hitbox (x, y, width, height)

    Methods
    -------
    draw(self, surface)
        Draws block on a given surface.
    """

    def __init__(self, respan_row, respawn_collumn, value, color):
        """
        The constructor for the BlockClass class

        ...

        Parameters
        ----------
        respawn_row : int
            row in which upper left corner of block is located
        respawn_collumn : int
            collumn in which upper left corner of block is located
        value : int
            after how many hits this block should disappear and how many points player should get after destroying it
        color : (int, int, int)
            RGB value representing block's color
        """

        self.row = respan_row
        self.collumn = respawn_collumn
        self.value = value
        self.center = (self.collumn + 31, (self.row) + 15)
        self.point_prize = value
        self.color = color 
        self.hitbox = (self.collumn, self.row, 62, 30)

    def draw(self, surface):
        """
        Draws block on a given surface.

        ...

        Parameters
        ----------
        surface : pygame.surface
            canvas to draw on
        """

        # draw.rect(where, color, (x, y, width, height))
        # self.collumn * 16 converts pixels to squares on gird
        # pygame.draw.rect(surface, self.colour, (self.collumn * 16,self.row * 16, 63, 31))
        pygame.draw.rect(surface, self.color, (self.collumn, self.row, 62, 30))
