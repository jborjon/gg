# utils.py
#
# GameGenerator is free to use, modify, and redistribute for any purpose
# that is both educational and non-commercial, as long as this paragraph
# remains unmodified and in its entirety in a prominent place in all
# significant portions of the final code. No warranty, express or
# implied, is made regarding the merchantability, fitness for a
# particular purpose, or any other aspect of the software contained in
# this module.

import os
import sys
import pygame
import gg.colors

_ERR_PREFIX = 'GG ERROR:'


def _load_image(file_name, directory=None, dest_object_name=None):
    """Load an image from the file system and return an image object.

    If an image can't be loaded for any reason (usually because the file
    or folder name specified is misspelled or the file itself is
    missing), return instead a small red square with a white question
    mark inside.

    The optional dest_object_name parameter is used for printing the
    name of the object that didn't receive the proper image if the file
    retrieval fails. It is recommended to use the proper article in the
    string passed, as in "the player" or "a full-screen image".
    """
    # Try to load the image through pygame
    try:
        # Check that the file name be valid
        if file_name is None:
            raise RuntimeError("An image file wasn't specified")

        if directory is None:
            path = file_name
        else:
            path = os.path.join(directory, file_name)

        image = pygame.image.load(path)

        # If the image has transparency, preserve it
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except RuntimeError as err:
        # If the image can't be loaded, use the Red Square of Doom
        image = _get_square_of_doom()

        if dest_object_name is None:
            err_message = str(err)
        else:
            loc_specifier = ''.join([' for ', dest_object_name, '.'])
            err_message = ''.join([str(err), loc_specifier])

        print(_ERR_PREFIX, err_message, os.linesep,
              ' ' * (len(_ERR_PREFIX) - 1),
              'Loaded the Red Square of Doom instead.', file=sys.stderr)

    return (image, image.get_rect())


def _blit_text_to_surface(text, surface, text_rect=None, surface_rect=None):
    """Center the text and blit it on the surface."""
    if text_rect is None:
        text_rect = text.get_rect()

    if surface_rect is None:
        surface_rect = surface.get_rect()

    text_rect.center = surface_rect.center
    surface.blit(text, text_rect)


def _get_surface(size, color=None):
    """Return a solid, rectangular surface and its rect."""
    # Convert unless pygame complains that the video mode isn't set
    try:
        surface = pygame.Surface(size).convert()
    except pygame.error:
        surface = pygame.Surface(size)

    if color is not None:
        surface.fill(color)

    return (surface, surface.get_rect())


def _get_rendered_text(font_obj, text, color):
    """Return pygame text and its rect."""
    text = font_obj.render(text, True, color)
    return (text, text.get_rect())


def _get_square_of_doom():
    """Return a red square surface with a white question mark inside.

    Useful as a replacement for images that cannot be loaded, so as to
    make it obvious to the programmer that something didn't go quite as
    expected.
    """
    square, square_rect = _get_surface((64, 64), gg.colors.RED)
    font = pygame.font.Font(None, 72)
    text, text_rect = _get_rendered_text(font, '?', gg.colors.WHITE)
    _blit_text_to_surface(text, square, text_rect, square_rect)
    return square
