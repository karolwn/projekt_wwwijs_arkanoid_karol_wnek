import pygame
from math import sqrt


class BallClass:
    """
    A class to represent a ball
    
    ...

    Atributes
    ---------
    radius : int
        ball's radius
    color : (int, int, int)
        RGB value representing ball's color
    pos_x : float 
        x coordinate of ball's center
    pos_y : float
        y coordinate of ball's center
    in_move : boolean
        defines whether ball is moving or not
    vel_x : float
        x axis velocity
    vel_y : float
        y axis velocity
    vel : float
        total velocity
    power : int
        tells how much damage the ball is dealing
    new_ball : boolean
        new ball flag, switched to False after launching the new ball 

    Methods
    -------
    draw(self, surface)
        Draws ball on a given surface.
    movement(self, keys, game_size)
        defines ball's movement
    pos_update(self, player)
        resets ball position to the starting one, (middle of the player)
    player_hit(self, hitbox_player, game_size_y)
        collision detection ball-player
    block_hit(self, hitbox_block)
        collision detection ball-block
    corner_hit(self, corner_x, corner_y)
        changes speed of ball after coliding with block's corner
    update_speed(self, speed_multi)
        updates ball' s speed using provided multiplier
    """

    radius = 10
    color = (200,200,200)
    in_move = False
    new_ball = True

    def __init__(self, player, game_size_y, speed, power, speed_x = 0.0):
        """
        The constructor for the BallClass class

        ...

        Parameters
        ----------
        player : PlayerClass
            used to determine ball's default x position
        game_size_y
            used to determine ball's default y position
        speed : float
            ball's total velocity
        power : int
            ball's power
        speed_x : folat
            ball's x velocity, by default 0
        """

        self.pos_x = (player.position * 16) + (8 * player.size)
        self.pos_y = game_size_y - 60 - 30
        self.vel_x = speed_x
        self.vel_y = sqrt(speed**2 - speed_x**2)
        self.vel = speed;
        self.power = power
    
    def draw(self, surface):
        """
        Draws ball on a given surface.

        ...

        Parameters
        ----------
        surface : pygame.surface
            canvas to draw on
        """

        # draw.circle(where, color, (x,y), radius)
        pygame.draw.circle(surface, self.color, (int(self.pos_x), int(self.pos_y)), self.radius)

    def movement(self, keys, game_size, bounce, dt):
        """
        Defines ball's movement and bouncing off the walls.

        ...

        Parameters
        ----------
        keys : pygame.keys.get_pressed()
            keys on the keyboard that were pressed by the player
        game_size : (int, int)
            tuple conatining game window size in pixels (e.g. 800 x 600) 
        bounce : pygame.mixer.Sound
            sound effect to play when ball bounces off the walls
        dt : int
            time in ms that took to process previous frame
        """

        if keys[pygame.K_SPACE]:
            self.in_move = True
            self.new_ball = False

        if self.in_move:
            self.pos_x += self.vel_x * dt / 1000
            self.pos_y -= self.vel_y * dt / 1000

            # right wall
            if self.pos_x > game_size[0] - self.radius / 2:
                self.pos_x = game_size[0] - self.radius / 2
                self.vel_x = -self.vel_x
                bounce.play()

            # left wall
            if self.pos_x < 5:
                self.pos_x = 5
                self.vel_x = -self.vel_x
                bounce.play()
            
            # ceiling
            if self.pos_y < 5:
                self.pos_y = 5
                self.vel_y = - self.vel_y
                bounce.play()


    def pos_update(self, player):
        """
        Resets ball position to the starting one, (middle of the player).

        ...

        Parameters
        ----------
        player :  PlayerClass
            used to determinate requred position
        """

        self.pos_x = (player.position * 16) + (8 * player.size)

    def player_hit(self, hitbox, game_size_y):
        """
        Collision detection ball-player.

        ...

        Parameters
        ----------
        hitbox : (int, int, int, int)
            tuple containing player's hitbox
        game_size_y : int
            height of the game window
        
        Returns
        -------
        True if hit else False : boolean 
        """

        # +10 / -10 buffer to encourage player to play more aggressively
        # -60: height of UI
        if hitbox[0] - 10 <= self.pos_x <= hitbox[0] + hitbox[2] + 10:
            if self.pos_y + self.radius >= game_size_y - 60 - hitbox[3]:
                return True
            else:
                return False
        return False

    def block_hit(self, box, dt):
        """
        Collision detection ball-block and reacting to it - velocity change.

        ...

        Parameters
        ----------
        hitbox : (int, int, int, int)
            tuple containing hitbox of block (left upper corner x, left upper corner y, width, height)
        dt : int
            time in ms that took to process previous frame

        Returns
        -------
        True if hit else False : boolean 

        """

        #    ______
        #   |      |
        #   ¯¯¯¯¯¯¯¯
        #      ∧
        if self.vel_y > 0 and box[0] <= self.pos_x <= box[0] + box[2]:
            if box[1] + box[3]  <= self.pos_y <= box[1] + box[3] + self.radius:
                self.pos_y = box[1] + box[3] + self.radius
                self.vel_y  = -self.vel_y

                self.pos_x += self.vel_x * dt/1000
                self.pos_y -= self.vel_y * dt/1000

                return True

        #      ∨
        #    ______
        #   |      |
        #   ¯¯¯¯¯¯¯¯
        if self.vel_y < 0 and box[0] <= self.pos_x <= box[0] + box[2]:
            if box[1] - self.radius <= self.pos_y <= box[1]:
                self.pos_y = box[1] - self.radius
                self.vel_y  = -self.vel_y

                self.pos_x += self.vel_x * dt/1000
                self.pos_y -= self.vel_y * dt/1000

                return True

        #     ______
        #  > |      |
        #    ¯¯¯¯¯¯¯¯
        if self.vel_x > 0 and box[1] <= self.pos_y <= box[1] + box[3]:
            if box[0] - self.radius <= self.pos_x <= box[0]:
                self.pos_x = box[0] - self.radius
                self.vel_x  = -self.vel_x

                self.pos_x += self.vel_x * dt/1000
                self.pos_y -= self.vel_y * dt/1000

                return True

        #    ______
        #   |      | <
        #   ¯¯¯¯¯¯¯¯
        if self.vel_x < 0 and box[1] <= self.pos_y <= box[1] + box[3]:
            if box[0] + box[2] <= self.pos_x <= box[0] + box[2] + self.radius:
                self.pos_x = box[0] + box[2]+ self.radius
                self.vel_x  = -self.vel_x

                self.pos_x += self.vel_x * dt/1000
                self.pos_y -= self.vel_y * dt/1000

                return True
        
        # upper left corner
        if self.vel_y < 0 and self.vel_x >= 0:
            if box[0] - self.radius <= self.pos_x < box[0] and box[1] - self.radius <= self.pos_y < box[1]:
                if (self.pos_x - box[0])**2 + (self.pos_y - box[1])**2 < self.radius ** 2:
                    self.corner_hit(box[0], box[1])

                    self.pos_x += self.vel_x * dt/1000
                    self.pos_y -= self.vel_y * dt/1000

                    return True
        
        # upper right corner
        if self.vel_y < 0 and self.vel_x <= 0:
            if box[0] + box[2] < self.pos_x <= box[0] + box[2] + self.radius and box[1] - self.radius <= self.pos_y < box[1]:
                if (self.pos_x - (box[0] + box[2]))**2 + (self.pos_y - box[1])**2 < self.radius ** 2:
                    self.corner_hit(box[0] + box[2], box[1])

                    self.pos_x += self.vel_x * dt/1000
                    self.pos_y -= self.vel_y * dt/1000

                    return True

        # bottom right corner
        if self.vel_y > 0 and self.vel_x <= 0:
            if box[0] + box[2] < self.pos_x <= box[0] + box[2] + self.radius and box[1] + box[3] < self.pos_y <= box[1] + box[3] + self.radius:
                if (self.pos_x - (box[0] + box[2]))**2 + (self.pos_y - (box[1] + box[3]))**2 < self.radius ** 2:
                    self.corner_hit(box[0] + box[2], box[1] + box[3])

                    self.pos_x += self.vel_x * dt/1000
                    self.pos_y -= self.vel_y * dt/1000

                    return True
        
        # bottom left corner
        if self.vel_y > 0 and self.vel_x >= 0:
            if box[0] - self.radius <= self.pos_x < box[0] and box[1] + box[3] < self.pos_y <= box[1] + box[3] + self.radius:
                if (self.pos_x - box[0])**2 + (self.pos_y - (box[1] + box[3]))**2 < self.radius ** 2:
                    self.corner_hit(box[0], box[1] + box[3])

                    self.pos_x += self.vel_x * dt/1000
                    self.pos_y -= self.vel_y * dt/1000

                    return True


    def corner_hit(self, corner_x, corner_y):
        """
        Changes speed of ball after coliding with block's corner

        '''

        Parameters
        ----------
        corner_x : int
            x coordinate of the corner
        corner_y : int
            y coordinate of the corner 
        """

        try:
            v1x = self.pos_x - corner_x
            v1y = self.pos_y - corner_y
            len = sqrt(v1x ** 2 + v1y ** 2)
            tx = v1x / len
            ty = v1y / len
            dot = (self.vel_x * tx + self.vel_y * ty) * 2
            self.vel_x = -self.vel_x + tx * dot
            self.vel_y = -self.vel_y + ty * dot

        # when len = 0, perfect hit
        except:
            self.vel_x = -self.vel_x
            self.vel_y = -self.vel_y

    def update_speed(self, speed_multi):
        """
        Updates ball' s speed using provided multiplier
        
        ...

        Parameters
        ----------

        speed_multi : int
            speed modifier in %
        """
        if  400 < sqrt(self.vel**2 - self.vel_x**2) < 1600:
            self.vel_x *= (1 + speed_multi / 100)
            self.vel_y *= (1 + speed_multi / 100)
            self.vel = sqrt(self.vel_x**2 + self.vel_y**2)
