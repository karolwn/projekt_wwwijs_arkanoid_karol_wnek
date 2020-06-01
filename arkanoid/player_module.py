import pygame

class PlayerClass:
    """
    Class defining player

    ...

    Atributes
    ---------
    lives : int
        how many lives are left
    points : int
        player's score
    size : int
        how big is the player
    color : (int, int, int)
        RGB value describing color
    position : int
        where does player start, x coordinate of the upper left corner
    position_bottom : int
        where does player start, y coordinate of the upper left corner
    hitbox : (int, int, int, int)
        tuple containig informations about player's hitbox (x, y, width, height)
    move_limitter : int
        limits speed of player's movement
    speed_mod : float
        modyfies player speed
    in_move : boolean
        describes player's ability to move

    Methods
    -------
    move(self, moveLimitter, keys, game_size_x)
        responds to pressed buttons (left arrow, right arrow)
    draw(self, surface)
        draws player on a given surface
    get_hitbox(self)
        returns player's current hitbox
    """
    speed_mod = 1.0
    lives = 3
    points = 0
    invert = 1
    color = (255, 255, 255)
    move_limitter = 1
    in_move = True

    def __init__(self, player_size, game_size):
        """
        The constructor for the PlayerClass class

        ...

        Parameters
        ----------
        player_size : int
            player's width
        game_size : (int, int)
            tuple containig widht and height of the game screen in pixels
        """

        self.size = player_size
        self.position = game_size[0] // 32 - self.size // 2
        self.position_bottom = game_size[1] - 60 - 16
        self.hitbox = (self.position * 16, self.position_bottom, self.size * 16 ,16)

    def move(self, move_limitter, keys, game_size_x, dt):
        """
        Responds to pressed buttons (left arrow, right arrow) and moves player in desired direction.

        ...

        Parameters
        ----------
        move_limitter : int
            limits speed of the movement in such way that player can move in every two frames instead of every frame
        keys : pygame.key
            presed keys
        game_size_x : int
            width of game window, used to determinate where the player should stop
        dt : int
            how long it took to render preavious frame
        """

        if keys[pygame.K_SPACE]:
            self.in_move = True

        if self.in_move:
            if keys[pygame.K_LEFT]:
                if self.move_limitter == 0:
                    self.move_limitter = move_limitter
                    self.position -= (50 * dt/1000) * self.invert * self.speed_mod
                    if self.position < 0:
                        self.position = 0
                    if self.position > (game_size_x // 16) - self.size:
                        self.position = (game_size_x // 16) - self.size

            if keys[pygame.K_RIGHT]:
                if self.move_limitter == 0:   
                    self.move_limitter = move_limitter   
                    self.position += (50 * dt/1000) * self.invert * self.speed_mod
                    if self.position < 0:
                        self.position = 0
                    if self.position > (game_size_x // 16) - self.size:
                        self.position = (game_size_x // 16) - self.size

    def draw(self, surface):
        """
        Draws player on a given surface.s

        ...

        Parameters
        ----------
        surface : pygame.surface
            canvas to draw on
        """

        # draw.rect(where, colour, (x,y,width, height))
        # self.collumn * 16 converts pixels to squares on gird
        pygame.draw.rect(surface, self.color, (int(self.position * 16), self.position_bottom, self.size * 16, 16))

    def get_hitbox(self):
        """
        Returns player's current hitbox

        ...

        Returns
        -------
        player's hitbox : (int, int, int, int)
            (x coordinate of the upper left corner, y coordinate of the upper left corner, width, height) 
        """

        return (self.position * 16, self.position_bottom, self.size * 16 ,16)

