# thumbnail.py
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


class Thumbnail(pygame.sprite.Sprite):
    """A size-reduced representation of a sprite.

    The size of the resulting sprite is determined by the height
    specified. The image is resized to that height, preserving the aspect
    ratio and thus the relative width.
    """

    def __init__(self, group, pos, new_height, image_file, image_dir=None):
        """Initialize the thumbnail."""
        pygame.sprite.Sprite.__init__(self, group)
        self.image, image_rect = gg.utils._load_image(image_file, image_dir,
                                                      'a thumbnail')

        aspect_ratio = image_rect.width / image_rect.height
        new_width = round(new_height * aspect_ratio)
        new_size = (new_width, new_height)

        # Scale the image
        try:
            self.image = pygame.transform.smoothscale(self.image, new_size)
        except ValueError:
            self.image = pygame.transform.scale(self.image, new_size)

        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        """Nothing is required except completeness :)"""
        pass
