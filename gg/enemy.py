# enemy.py
#
# GameGenerator is free to use, modify, and redistribute for any purpose
# that is both educational and non-commercial, as long as this paragraph
# remains unmodified and in its entirety in a prominent place in all
# significant portions of the final code. No warranty, express or
# implied, is made regarding the merchantability, fitness for a
# particular purpose, or any other aspect of the software contained in
# this module.

import random
import pygame
import gg.utils


class Enemy(pygame.sprite.DirtySprite):
    """A flying bad guy to be defeated by the player.

    When hit, the enemy doesn't really die, but is just reset, kept out
    of the game sleeping for a random interval of a few seconds, and
    then put back into the game, so as to avoid initializing new objects
    every time and adding them to the container, which can be slow.

    The minimum speed value is 100. If a smaller value is passed, it is
    automatically converted to 100.
    """
    LEFT = 0
    RIGHT = 1

    def __init__(self, group, bomb_data, screen_rect, boundaries, image_file,
                 image_dir=None, speed=600):
        """Set initial values for the enemy."""
        pygame.sprite.DirtySprite.__init__(self, group)
        self.image, self.rect = gg.utils._load_image(image_file, image_dir,
                                                     'the enemy')
        self.dirty = 2
        self._bomb_data = bomb_data
        self._screen_rect = screen_rect
        self._top_boundary, self._bottom_boundary = boundaries
        self._is_awake = bool(random.randint(0, 1))    # does it start awake?
        self._direction = self.RIGHT
        self._previous_dir = self.RIGHT
        self._wake_up_timer = 0.0
        self._target_point = None
        self._is_bomb_dropped = False

        if speed >= 100:
            self._speed = speed
        else:
            self._speed = 100

        if self._is_awake:
            self._wake_up()
        else:
            self.knock_out()

    def update(self, delta_time):
        """Move the enemy in the appropriate direction.

        If the enemy is knocked out, decrement the wake-up timer until
        it's less than or equal to zero. When the timer runs out, awaken
        the enemy in a new location.
        """
        if self._is_awake:
            if self._direction == self.LEFT:
                self.rect.x -= self._speed * delta_time
            elif self._direction == self.RIGHT:
                self.rect.x += self._speed * delta_time
            else:
                raise RuntimeError(''.join(["Invalid enemy direction '",
                                            str(self._direction), "'."]))

            # Disappear if we've gone off a screen edge
            if self.rect.right < 0 or self.rect.left > self._screen_rect.right:
                self.knock_out()
                return

            # Drop the bomb if we're at the target point
            if (self.rect.collidepoint(self._target_point) and
                not self._is_bomb_dropped):
                self._drop_bomb()
        elif self._wake_up_timer > 0:
            self._wake_up_timer -= delta_time
        else:
            self._wake_up()

    def knock_out(self):
        """Put the enemy to sleep and start a timer to keep him out."""
        self._is_awake = False
        self._previous_dir = self._direction
        self.rect.right = -1    # to keep the enemy out of the screen
        self._wake_up_timer = random.randint(1, 5)    # stay out for 1-5 secs

    def _wake_up(self):
        """Bring the enemy back on the proper side of the screen."""
        self._is_awake = True
        self._is_bomb_dropped = False
        self._direction = random.randint(0, 1)

        # Put the enemy back on the appropriate side of the screen
        if self._direction == self.RIGHT:
            self.rect.right = -1
        elif self._direction == self.LEFT:
            self.rect.left = self._screen_rect.right + 1
        else:
            raise RuntimeError(''.join(["Invalid enemy direction '",
                                        str(self._direction), "'."]))

        if self._direction != self._previous_dir:
            self.image = pygame.transform.flip(self.image, True, False)

        # Pick a random y-position within the valid corridor
        try:
            self.rect.y = random.randint(self._top_boundary,
                                         self._bottom_boundary
                                         - self.rect.height)
        except ValueError:
            self.rect.y = 0

        # Pick a point to drop the bomb
        self._target_point = (random.randint(16, self._screen_rect.width - 16),
                              self.rect.centery)

    def _drop_bomb(self):
        """Drop a bomb when the bombing point is reached."""
        new_bomb = gg.ammo.Ammo(
                self._bomb_data['group'],
                self._bomb_data['screen_rect'],
                self.rect.center,
                self._bomb_data['image_file'],
                self._bomb_data['image_dir'],
                not self._bomb_data['is_direction_up'],
                self._bomb_data['speed']
            )
        self._is_bomb_dropped = True
