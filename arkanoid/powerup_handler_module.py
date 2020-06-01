import random
from ball_module import *

def powerup_handler(powerups, blocks, balls, player, hitmarker, pow, dt, size, ball_speed, ball_power, keys):
    """
    This functions handles powerups collected by the users by checking their type_code

    ...

    Parameters
    ----------
    powerups : [PowerupClass]
        list that contains all visible powerups
    blocks : [BlockClass]
        list containing blocks
    balls : [BallClass]
        list containing balls
    player : PlayerClass
        player
    hitmarker : pygame.mixer.Sound
        hitmarker sound
    pow : pygame.mxer.Sound
        sound to be played when the user picks up a powerup
    dt : int
        how long it took to render previous frame
    size : (int, int)
        game window size
    ball_speed : int
        ball's total velocity
    ball_power : int
        ball's damage
    keys : pygame.keys.get_pressed()
        pressed keys

    Returns
    -------
    powerups : [PowerupClass]
        list that contains all visible powerups
    balls : [BallClass]
        list containing balls
    blocks : [BlockClass]
        list containing blocks
    """

    if len(powerups) > 0:
        for powerup in powerups:
            powerup.move(dt, keys)
            if powerup.type_code == 66:
                if powerup.y < 0:
                    powerups.remove(powerup)
                for block in blocks:
                    if block.hitbox[0] <= powerup.x + 8 <= block.hitbox[0] + block.hitbox[2]:
                        if powerup.y < block.hitbox[1] + block.hitbox[1]:
                            player.points += block.point_prize * 100
                            hitmarker.play()
                            blocks.remove(block)
        
            if powerup.y > size[1] - 60:
                powerups.remove(powerup)
            if powerup.is_caught(player.get_hitbox()):
                if powerup.type_code == 1:  # ball's power x2 multiplayer
                    pow.play()
                    for ball in balls:
                        ball.power *= 2
                        ball.color = (255,0,0)
                    powerups.remove(powerup)

                elif powerup.type_code == 2: # double ball
                    pow.play()
                    if len(balls) < 5:
                        balls.append(BallClass(player, size[1], ball_speed, ball_power, ball_speed / 20))
                        balls.append(BallClass(player, size[1], ball_speed, ball_power, -ball_speed / 20))
                    powerups.remove(powerup)

                elif powerup.type_code == 3: # triple ball
                    pow.play()
                    if len(balls) < 4:
                        balls.append(BallClass(player, size[1], ball_speed, ball_power, ball_speed / 20))
                        balls.append(BallClass(player, size[1], ball_speed, ball_power))
                        balls.append(BallClass(player, size[1], ball_speed, ball_power, -ball_speed / 20))
                    powerups.remove(powerup)

                elif powerup.type_code == 4: # APFSDS
                    pow.play()
                    powerup.type_code = 66
                    powerup.vel = -2000

                elif powerup.type_code == 5: # larger player
                    pow.play()
                    player.size += 1
                    powerups.remove(powerup)

                elif powerup.type_code == 6: # smaller player
                    pow.play()
                    player.size -= 1 if player.size >= 2 else 0
                    powerups.remove(powerup)

                elif powerup.type_code == 7: # faster ball
                    pow.play()
                    player.speed_mod += 0.1 if player.speed_mod < 2 else 0
                    for ball in balls:
                        ball.update_speed(10)
                    powerups.remove(powerup)

                elif powerup.type_code == 8: # slower ball
                    pow.play()
                    player.speed_mod -= 0.1 if player.speed_mod > 1 else 0
                    for ball in balls:
                        ball.update_speed(-10)
                    powerups.remove(powerup)

                elif powerup.type_code == 9: # +1up
                    pow.play()
                    player.lives += 1
                    powerups.remove(powerup)

                elif powerup.type_code == 10: # -1up
                    pow.play()
                    player.lives -= 1
                    powerups.remove(powerup)

                elif powerup.type_code == 11: # inverted controls
                    pow.play()
                    player.invert *= -1
                    powerups.remove(powerup)

                else:                         # random explosion
                    pow.play()
                    for i in range(0, random.randint(1, 5)):
                        block = blocks.pop(random.randint(1,len(blocks)) - 1)
                        player.points += block.point_prize * 100
                        hitmarker.play()
                    powerups.remove(powerup)

    return powerups, balls, blocks
