import pygame

class PowerupClass:
    """
    This is a powerup class used to represent single powerup

    ...

    Atributes
    ---------
    type_code : int
        it describes what type of power up is this object
    duration : int
        how long does the effect last
    vel : int
        how fast does it fall down
    colors : [(int, int, int)]
        list that contains tuples containing RGB value
    x : int
        x coordinate
    y : int
        y coordinate
    in_move : boolean
        describes powerup's ability to move

    Methods
    -------
    draw(self, surface)
        draws powerup on a given surface
    is_caught(self, player)
        decides whether player has caugth it
    move(self, dt, keys)
        defines powerup's movement
    """
    vel = 400
    colors = [(89, 84, 214), (0, 187, 173), (0, 173, 108), (189, 189, 189), (0, 140, 249), (235, 172, 35), (209, 99, 230), (0, 198, 248), (0, 110, 0), (184, 0, 88), (255, 146, 135), (178, 69, 2)]
    in_move = True

    def __init__(self, type_code, respawn_point):
        """
        The constructor for the PowerupClass class

        ...

        Parameters
        ----------
        type_code : int
            what powerup is it
                1:  ball's power x2 multiplayer
                2:  double ball
                3:  triple ball
                4:  APFSDS
                5:  larger player
                6:  smaller player
                7:  faster ball
                8:  slower ball
                9:  +1up
                10: -1up
                11: inverted controls
                12: random explosion
        respawn_point : (int, int)
            tuple containing starting position
        """

        self.type_code = type_code
        self.x = respawn_point[0]
        self.y = respawn_point[1]

    def draw(self, surface):
        """
        Draws powerup on a given surface.

        ...

        Parameters
        ----------
        surface : pygame.surface
            canvas to draw on
        """

        # draw.rect(where, color, (x, y, width, height))
        # self.collumn * 16 converts pixels to squares on gird
        # pygame.draw.rect(surface, self.colour, (self.collumn * 16,self.row * 16, 63, 31))
        try:
            pygame.draw.rect(surface, self.colors[self.type_code-1], (self.x, self.y, 16, 16))
        except:
            pygame.draw.rect(surface, self.colors[3], (self.x, self.y, 16, 16))
    def is_caught(self, player):
        """
        Decides whether player has caugth it.

        ...

        Atributes
        ---------
        player : (int, int, int, int)
            informations about player's hitbox

        Returns
        -------
        True if caught else False : boolean
        """
        if player[0] - 8 <= self.x <= player[0] + player[2] + 8:
            if  player[1] <= self.y + 8 <= player[1] + player[3]:
                return True
            else:
                return False
        return False

    def move(self, dt, keys):
        """
        Defines powerup's movement.

        ...

        Parameters
        ----------
        dt : int
            time in ms that took to process previous frame
        keys : pygame.keys.get_pressed()
            keys on the keyboard that were pressed by the player
        """
        if keys[pygame.K_SPACE]:
            self.in_move = True

        if self.in_move:
            self.y += self.vel * dt / 1000





