# player.py
#
# GameGenerator is free to use, modify, and redistribute for any purpose
# that is both educational and non-commercial, as long as this paragraph
# remains unmodified and in its entirety in a prominent place in all
# significant portions of the final code. No warranty, express or
# implied, is made regarding the merchantability, fitness for a
# particular purpose, or any other aspect of the software contained in
# this module.

import pygame
import gg.utils


class Player(pygame.sprite.DirtySprite):
    """The anti-aircraft artillery piece controlled by the player.

    The minimum speed value is 100. If a smaller value is passed, it is
    automatically converted to 100.
    """
    LEFT = 0
    RIGHT = 1

    def __init__(self, missile_data, screen_rect, image_file, image_dir=None,
                 initial_x_pos=None, y_pos=0, speed=600, num_lives=3,
                 max_shots=10, has_sprite_dir=True):
        """Set initial values for the player."""
        pygame.sprite.DirtySprite.__init__(self)
        self.MAX_SHOTS = max_shots
        self.num_lives = num_lives
        self.image, self.rect = gg.utils._load_image(image_file,
                                                     image_dir, 'the player')
        self.rect.y = y_pos
        self.is_alive = True
        self.is_moving_left = False
        self.is_moving_right = False
        self._missile_data = missile_data
        self._screen_rect = screen_rect
        self._initial_x_pos = initial_x_pos
        self._has_sprite_dir = has_sprite_dir

        if self._has_sprite_dir:
            self._previous_dir = self.RIGHT    # just so it works right
            self._current_dir = self.RIGHT

        if speed > 100:
            self._speed = speed
        else:
            self._speed = 100

        if max_shots > 0:
            self.shots_left = max_shots
        else:
            self.shots_left = 1    # any number greater than zero will do

        self._reset()

    def update(self, delta_time):
        """Move the player to the left or right."""
        if not self.is_alive:
            return

        # Flip the sprite if necessary
        if self._has_sprite_dir:
            if self.is_moving_right:
                self._current_dir = self.RIGHT
            elif self.is_moving_left:
                self._current_dir = self.LEFT

            if self._current_dir != self._previous_dir:
                self.image = pygame.transform.flip(self.image, True, False)

            self._previous_dir = self._current_dir

        # Move the player
        if self.is_moving_right:
            self.rect.x += self._speed * delta_time
            self.dirty = 1
        elif self.is_moving_left:
            self.rect.x -= self._speed * delta_time
            self.dirty = 1

    def shoot(self):
        """Create a new, moving ammo object."""
        if self.shots_left > 0:
            new_missile = gg.ammo.Ammo(
                self._missile_data['group'],
                self._missile_data['screen_rect'],
                self.rect.center,
                self._missile_data['image_file'],
                self._missile_data['image_dir'],
                self._missile_data['is_direction_up'],
                self._missile_data['speed']
            )

            if self.MAX_SHOTS > 0:
                self.shots_left -= 1

    def reload(self):
        """Bring the amount of ammo back to the maximum."""
        if self.shots_left < self.MAX_SHOTS:
            self.shots_left = self.MAX_SHOTS

    def knock_out(self):
        """Lose a life and reset to the starting position."""
        # Hint: make the number of lives 0 to become invincible
        if self.num_lives != 0:
            self.num_lives -= 1
            if self.num_lives <= 0:
                self.is_alive = False
                return
            self._reset()

    def _reset(self):
        """Set the player on its starting position."""
        if self._initial_x_pos is None:
            self.rect.centerx = self._screen_rect.centerx
        else:
            self.rect.x = self._initial_x_pos
