# groundobject.py
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


class GroundObject(pygame.sprite.Sprite):
    """An immobile ground structure to be defended by the player."""

    def __init__(self, group, pos, image_file,
                 razed_image_file=None, image_dir=None):
        """Initialize the ground object."""
        pygame.sprite.Sprite.__init__(self, group)
        self.image, self.rect = gg.utils._load_image(image_file, image_dir,
                                                     'a ground object')
        self._razed_image_file = razed_image_file
        self._image_dir = image_dir
        self.is_razed = False
        self.rect.topleft = pos

    def update(self):
        """Check if the building is still standing."""
        if self.is_razed:
            if self._razed_image_file is None:
                self.kill()
            else:
                self.image = gg.utils._load_image(self._razed_image_file,
                                                  self._image_dir,
                                                  'a razed ground object')[0]
