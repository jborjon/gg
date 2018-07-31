# ammo.py
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


class Ammo(pygame.sprite.DirtySprite):
    """An object thrown at an opponent by someone in the game."""

    def __init__(self, group, screen_rect, initial_center_pos, image_file,
                 image_dir=None, is_direction_up=False, speed=800):
        """Set initial values for the ammo."""
        pygame.sprite.DirtySprite.__init__(self, group)
        self.image, self.rect = gg.utils._load_image(image_file, image_dir,
                                                     'ammo')
        self.dirty = 2
        self._is_direction_up = is_direction_up
        self._speed = speed

        if not is_direction_up:
            self._screen_bottom = screen_rect.bottom

        self.rect.center = initial_center_pos

    def update(self, delta_time):
        """Move the ammo up or down."""
        if self._is_direction_up and self.rect.bottom > 0:
            self.rect.y -= self._speed * delta_time
        elif not self._is_direction_up and self.rect.top < self._screen_bottom:
            self.rect.y += self._speed * delta_time
        else:
            self.kill()
