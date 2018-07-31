# gg.py
#
# This file contains the GameGenerator (GG) module, which needs to be
# imported in order to create your very own Flak game.
#
# If you're interested in figuring out how this code works, go ahead:
# look through it, change it - even break it if you need to. You may run
# into stuff we didn't talk about in class, but don't let that stop you.
# Just Google around :)
#
# While having each Pyhon class in its own separate file can make for
# neater code, we want to keep the number of files for this project as
# small as possible, so all the classes and supporting functions of
# GG are huddled together in this module.
#
# GameGenerator is free to use, modify, and redistribute for any purpose
# that is both educational and non-commercial, as long as this paragraph
# remains unmodified and in its entirety in a prominent place in all
# significant portions of the final code. No warranty, express or
# implied, is made regarding the merchantability, fitness for a
# particular purpose, or any other aspect of the software contained in
# this module.
#
# Okay, enough preamble. Enjoy!

"""GameGenerator - A simple 2D game engine for creating Flak games.

GG amounts to a small, simple game engine for making little Flak-style
2D games. Its intended clients are Mr. Borjon's awesome 6th-grade
students.

Flak, the style of game supported by GG, consists of a player on the
ground (the bottom of the screen) attempting to shoot down enemy planes
performing their bombing runs. The player and the ground structures the
player defends must survive, with the player reloading every few shots
when out of ammo (with unlimited reloads). It's fast-paced, challenging,
and exciting!
"""

# This is information about the module in this file, not game code
__author__ = 'Mr. Joseph Borjon'
__email__ = 'work@josephborjon.com'
__license__ = 'Free with restrictions (see file header)'
__version__ = '0.1.0'
__credits__ = ['Joseph Borjon']
__date__ = '2017-11-13'
__status__ = 'Development'

_ERR_PREFIX = 'GG ERROR:'


import os
import sys
import random
import struct

try:
    import pygame
except ImportError as err:
    print(_ERR_PREFIX, err, ':_( Terminating game.', file=sys.stderr)
    sys.exit(1)

# Some basic colors for you to use if you so choose
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
DARK_GRAY = (31, 31, 31)
MEDIUM_DARK_GRAY = (63, 63, 63)
MEDIUM_LIGHT_GRAY = (180, 180, 180)
LIGHT_GRAY = (236, 236, 236)
RED = (255, 0, 0)
MAROON = (102, 0, 0)
PINK = (255, 204, 204)
GREEN = (0, 255, 0)
DARK_GREEN = (51, 102, 0)
LIGHT_GREEN = (204, 255, 153)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 51, 102)
LIGHT_BLUE = (153, 204, 255)
CYAN = (0, 255, 255)
TEAL = (0, 153, 153)
MAGENTA = (255, 0, 255)
FUCSIA = (255, 0, 127)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
BROWN = (153, 76, 0)
PURPLE = (102, 0, 204)


class Game:
    """The entire environment for creating and playing a Flak game.

    The client (you) should set his or her own values for the game
    attributes, but they are set up by default so that everything except
    images works out of the box.

    Modifiable attributes:

    -name: the name of the game, displayed on the game title bar.
    -images_dir: the name of the directory where the images are.
    -window_icon: file name of the icon to display next to the name.
    -splash_image: the image that covers the screen at the beginning.
    -screen_width: the window width in pixels if not fullscreen.
    -aspect_ratio: the aspect ratio of the window if not fullscreen.
    -is_fullscreen: whether the window covers the entire screen.
    -font_color: the color of the text that appears on the screen.
    -screen_font_size: the point size of the info text on the screen.
    -background_color: a solid color used if no image is specified.
    -background_image: file name of the image to put as background.
    -player_image: the image file for the player object.
    -player_num_lives: number of tries the player gets before losing.
    -player_num_shots: number of shots per reload. 0 means no reloading.
    -player_speed: how far the player moves left or right in one second.
    -player_x_pos: the initial x-coordinate of the player's top left.
    -player_y_pos: the initial y-coordinate of the player's top left.
    -has_player_sprite_dir: flip the player sprite when moving?
    -missile_image: the image file for the missile fired by the player.
    -missile_speed: how fast the player missile travels.
    -is_missile_upward: does the missile move upward? Down otherwise.
    -enemy_image: the image for all the enemy objects.
    -enemy_speed: how fast the enemy airplanes move.
    -enemy_count: max number of enemies on the screen at any given time.
    -enemy_top_edge: top of the boundary where enemies can spawn.
    -enemy_bottom_edge: bottom of the boundary where enemies can spawn.
    -bomb_image: the image file for the bomb dropped by the enemy.
    -bomb_speed: how fast the enemy bombs travel.
    -is_bomb_downward: does the bomb move downward? Up otherwise.
    -building_image: the image file for the ground structure objects.
    -building_razed_image: optional image for buildings that are hit.
    -building_count: how many buildings to have on the screen.
    -score_pos: the position where the score is displayed on the screen.
    -score_factor: how many points the player gets per hit.
    -score_loss_factor: points lost when a building is razed.
    -high_score_pos: the position where the high score is displayed.
    -num_lives_pos: the location of the player's remaining lives panel.
    -num_shots_pos: the location of the player's remaining shots panel.
    -thumbnails_height: the height of the lives and shots thumbnails.
    -message_high_score: message to show when the player gets highscore.
    -message_game_over: message to show when the player loses.
    -keys_move_left: list of keys that move the player left.
    -keys_move_right: list of keys that move the player right.
    -keys_shoot: list of keys that fire the missile.
    -keys_reload_ammo: list of keys that reload the ammo when out.
    -keys_pause: list of keys that pause the game.

    Client-invoked method:

    -run(): once all the modifiable attributes are set as desired, call
            this method to start the game.
    """

    def __init__(self):
        """Set default values for all the game attributes."""
        self.TARGET_FPS = 60

        # Modifiable game attributes
        self.name = 'GG Flak'
        self.images_dir = None
        self.window_icon = None
        self.splash_image = None
        self.screen_width = 800
        self.aspect_ratio = 1.7778
        self.is_fullscreen = False
        self.font_color = WHITE
        self.screen_font_size = 36
        self.background_color = BLACK
        self.background_image = None
        self.player_image = None
        self.player_num_lives = 3
        self.player_num_shots = 10
        self.player_speed = 800
        self.player_x_pos = None
        self.player_y_pos = None
        self.has_player_sprite_dir = True
        self.missile_image = None
        self.missile_speed = 2000
        self.is_missile_upward = True
        self.enemy_image = None
        self.enemy_speed = 600
        self.enemy_count = 5
        self.enemy_top_edge = None
        self.enemy_bottom_edge = None
        self.bomb_image = None
        self.bomb_speed = 800
        self.is_bomb_downward = True
        self.building_image = None
        self.building_razed_image = None
        self.building_count = 4
        self.building_y_pos = None
        self.score_pos = (10, 10)
        self.score_factor = 1
        self.score_loss_factor = 10
        self.high_score_pos = None
        self.num_lives_pos = (10, 40)
        self.num_shots_pos = (10, 74)
        self.thumbnails_height = 24
        self.message_high_score = 'You beat the high score!'
        self.message_game_over = 'Game over'
        self.keys_move_left = [pygame.K_LEFT]
        self.keys_move_right = [pygame.K_RIGHT]
        self.keys_shoot = [pygame.K_SPACE]
        self.keys_reload_ammo = [pygame.K_LCTRL, pygame.K_RCTRL]
        self.keys_pause = [pygame.K_p, pygame.K_PAUSE]

        # Attributes you shouldn't change from your own code
        self._screen = None
        self._screen_rect = None
        self._screen_height = None
        self._background_surf = None
        self._screen_font = None
        self._is_still_playing = True
        self._is_main_loop_running = True
        self._is_paused = False
        self._is_pause_displayed = False
        self._is_screen_info_shown = False
        self._keyboard_state = None
        self._player = None
        self._player_thumbnails = []
        self._data_dir = 'gamedata'
        self._data_file = os.path.join(self._data_dir, 'game.dat')
        self._score = None
        self._score_text = None
        self._score_rect = None
        self._high_score = 0
        self._high_score_text = None
        self._high_score_rect = None
        self._modal_text_font = None
        self._enemy_group = None
        self._missile_group = None
        self._bomb_group = None
        self._building_group = None
        self._thumbnail_group = None
        self._missile_thumbnails = []
        self._buildings_left = self.building_count
        self._clock = None

    def run(self):
        """Start the game and keep it going.

        Initialize all the pertinent game objects and then run the main
        game loop.
        """
        # Initialize the game environment
        self._init_environment()

        # Display the splash screen if one is given
        if self.splash_image is not None:
            self._display_splash_screen(self._screen)

        # Begin playing the game
        while self._is_still_playing:
            self._init_new_game()

            # The main loop
            self._run_main_loop()

            # Post-loop work: update the high score, etc.
            if self._score > self._high_score:
                self._update_high_score()
                has_high_score = True
            else:
                has_high_score = False

            if self._player.is_alive and self._buildings_left > 0:
                end_message = None
            else:
                if has_high_score:
                    end_message = self.message_high_score
                else:
                    end_message = self.message_game_over

            if end_message is not None:
                self._display_modal_text(end_message)
                self._prompt_play_again()

        # Here the player has exited both loops
        # Quit pygame once we're done with itnmiuy    zzzcucv
        # (I meant to say just "with it," but my 3-year-old disagreed)
        pygame.quit()

    def _run_main_loop(self):
        """Run the main loop of the game.

        This is it - where the magic of the game happens.
        """
        MAX_FPS = self.TARGET_FPS
        delta_time = 0
        self._clock = pygame.time.Clock()

        # Start the loop
        while (self._is_main_loop_running and
               self._player.is_alive and self._buildings_left > 0):
            has_score_changed = False

            if not self._is_paused:
                # Check if the player is hit by a bomb
                if pygame.sprite.spritecollide(self._player,
                                               self._bomb_group, True):
                    self._player.knock_out()
                    self._thumbnail_group.remove(self._player_thumbnails.pop())

                # Check for bomb hits on the buildings
                for building in pygame.sprite.groupcollide(
                    self._building_group, self._bomb_group, False, True):
                    if not building.is_razed:
                        building.is_razed = True
                        self._buildings_left -= 1
                        self._score -= self.score_loss_factor

                    if not has_score_changed:
                        has_score_changed = True

                # Check for missile hits on the enemies
                for enemy in pygame.sprite.groupcollide(self._enemy_group,
                                                        self._missile_group,
                                                        False, True):
                    enemy.knock_out()
                    self._score += self.score_factor
                    if not has_score_changed:
                        has_score_changed = True

                # Check for missile hits on the bombs
                for bomb in pygame.sprite.groupcollide(self._bomb_group,
                                                       self._missile_group,
                                                       True, True):
                    self._score += self.score_factor
                    if not has_score_changed:
                        has_score_changed = True

                # Update the frame
                self._screen.blit(self._background_surf, (0, 0))

                self._bomb_group.update(delta_time)
                bomb_rects = self._bomb_group.draw(self._screen)

                self._missile_group.update(delta_time)
                missile_rects = self._missile_group.draw(self._screen)

                self._enemy_group.update(delta_time)
                enemy_rects = self._enemy_group.draw(self._screen)

                self._building_group.update()
                building_rects = self._building_group.draw(self._screen)

                if self._player.is_alive:
                    self._screen.blit(self._player.image, self._player.rect)

                self._blit_current_score(has_score_changed)
                self._screen.blit(self._high_score_text, self.high_score_pos)

                thumbnail_rects = self._thumbnail_group.draw(self._screen)

                if self._is_screen_info_shown:
                    info_rects = self._blit_screen_info(self._clock.get_fps())
                else:
                    info_rects = ()

                # Draw the updates
                pygame.display.flip()
            elif not self._is_pause_displayed:
                self._display_pause_message()

            # Handle the player's input
            self._handle_input(delta_time)

            # Make sure we don't go above the target frame rate
            delta_time = self._clock.tick(MAX_FPS) / 1000.0

    def _init_environment(self):
        """Initialize modules and values necessary to play the game."""
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption(self.name)
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP,
                                  pygame.MOUSEBUTTONUP, pygame.QUIT])

        # Give the window a custom icon if one was specified
        if self.window_icon is not None:
            self._set_window_icon()

        # Initialize the screen
        if self.is_fullscreen:
            scr_flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            self._screen = pygame.display.set_mode((0, 0), scr_flags)
        else:
            self._set_screen_height()
            self._screen = pygame.display.set_mode((self.screen_width,
                                                    self._screen_height))
        self._screen.set_alpha(None, pygame.RLEACCEL)
        self._screen_rect = self._screen.get_rect()
        self._screen_font = pygame.font.Font(None, self.screen_font_size)
        self._modal_text_font = pygame.font.Font(None, 72)

        # Initialize the background
        self._background_surf = _get_surface(self._screen.get_size())[0]
        self._background_surf.set_alpha(None, pygame.RLEACCEL)

        # Blit the background onto the screen
        if self.background_image is None:
            self._background_surf.fill(self.background_color)
        else:
            bg_image, bg_rect = self._fit_image_to_screen(
                                self.background_image)
            self._background_surf.blit(bg_image, bg_rect)

        # Read the high score
        self._read_high_score()

    def _init_new_game(self):
        """Initialize the sprites at the beginning of the game."""
        # Create the groups
        self._enemy_group = pygame.sprite.LayeredDirty()
        self._missile_group = pygame.sprite.LayeredDirty()
        self._bomb_group = pygame.sprite.LayeredDirty()
        self._building_group = pygame.sprite.RenderUpdates()
        self._thumbnail_group = pygame.sprite.RenderUpdates()

        # Get the groups ready for drawing
        self._enemy_group.clear(self._screen, self._background_surf)
        self._missile_group.clear(self._screen, self._background_surf)
        self._bomb_group.clear(self._screen, self._background_surf)
        self._building_group.clear(self._screen, self._background_surf)
        self._thumbnail_group.clear(self._screen, self._background_surf)

        # Data to pass to the player to create missiles
        missile_data = {
            'group': self._missile_group,
            'screen_rect': self._screen_rect,
            'image_file': self.missile_image,
            'image_dir': self.images_dir,
            'is_direction_up': self.is_missile_upward,
            'speed': self.missile_speed,
        }

        # Put the player 75% of the way down the screen
        if self.player_y_pos is None:
            self.player_y_pos = self._screen_rect.height * 0.75

        self._player = Player(missile_data, self._screen_rect,
                              self.player_image, self.images_dir,
                              self.player_x_pos, self.player_y_pos,
                              self.player_speed, self.player_num_lives,
                              self.player_num_shots,
                              self.has_player_sprite_dir)

        # The bad guys
        if self.enemy_top_edge is None:
            self.enemy_top_edge = 0

        # Allow enemies to be only on the top half of the screen
        if self.enemy_bottom_edge is None:
            self.enemy_bottom_edge = round(self._screen_rect.height / 2)

        enemy_boundaries = (self.enemy_top_edge, self.enemy_bottom_edge)

        # Data to pass to the enemies to create bombs
        bomb_data = {
            'group': self._bomb_group,
            'screen_rect': self._screen_rect,
            'image_file': self.bomb_image,
            'image_dir': self.images_dir,
            'is_direction_up': self.is_bomb_downward,
            'speed': self.bomb_speed,
        }

        # Create these stinkin' guys
        for i in range(self.enemy_count):
            Enemy(self._enemy_group, bomb_data, self._screen_rect,
                  enemy_boundaries, self.enemy_image, self.images_dir,
                  self.enemy_speed)

        # Place the buildings at regular intervals
        building_rect = _load_image(self.building_image, self.images_dir,
                                    'the building')[1]
        building_width = building_rect.width
        building_interval = ((self._screen_rect.width - building_width
                              * self.building_count) / self.building_count)
        building_x_pos = building_interval / 2

        if self.building_y_pos is None:
            self.building_y_pos = (self._screen_rect.height
                                   - building_rect.height - 10)

        for i in range(self.building_count):
            building_pos = (building_x_pos, self.building_y_pos)

            GroundObject(self._building_group, building_pos,
                         self.building_image, self.building_razed_image,
                         self.images_dir)

            building_x_pos += building_interval + building_width

        # Keep track of the buildings we lose
        self._buildings_left = self.building_count

        # Reset the score
        self._score = 0

        # First call, to ensure it works properly later
        self._blit_current_score(True)

        # Position the high score
        high_score_text = ''.join(['High score: ', str(self._high_score)])
        self._high_score_text = self._screen_font.render(high_score_text, True,
                                                         self.font_color)
        self._high_score_rect = self._high_score_text.get_rect()

        if self.high_score_pos is None:
            self._high_score_rect.centerx = self._screen_rect.centerx
            self.high_score_pos = (self._high_score_rect.x, 10)

        self._high_score_rect.topleft = self.high_score_pos

        # Create the thumbnails for the number of lives
        self._create_thumbnails(self._player_thumbnails, self.num_lives_pos,
                                self.player_image, self.player_num_lives)

        # Create the thumbnails for the number of shots if not unlimited
        if self._player.MAX_SHOTS > 0:
            self._create_thumbnails(self._missile_thumbnails,
                                    self.num_shots_pos, self.missile_image,
                                    self._player.shots_left)

    def _create_thumbnails(self, thumb_list, pos, image_file, num_thumbs):
        """Create the thumbnails and add them to their container."""
        for i in range(num_thumbs):
            if i == 0:
                thumbnail_pos = pos
            else:
                thumbnail_pos = (thumbnail_pos[0]
                                 + last_thumbnail.rect.width + 6,
                                 thumbnail_pos[1])

            last_thumbnail = Thumbnail(self._thumbnail_group, thumbnail_pos,
                                       self.thumbnails_height, image_file,
                                       self.images_dir)
            thumb_list.append(last_thumbnail)

    def _set_window_icon(self):
        """Change the default pygame icon on the game window."""
        ICON_SIZE = (32, 32)

        try:
            if self.images_dir is None:
                path = self.window_icon
                window_icon = pygame.image.load(self.window_icon)
            else:
                path = os.path.join(self.images_dir, self.window_icon)
                window_icon = pygame.image.load(path)

            try:
                window_icon = pygame.transform.smoothscale(window_icon,
                                                           ICON_SIZE)
            except ValueError:
                window_icon = pygame.transform.scale(window_icon, ICON_SIZE)
        except RuntimeError:
            # Can't load the icon, so use a replacement square
            window_icon = _get_square_of_doom()
            print(_ERR_PREFIX, "Couldn't load the icon", path, file=sys.stderr)

        pygame.display.set_icon(window_icon)

    def _set_screen_height(self):
        """Set the window height based on the width and aspect ratio."""
        self._screen_height = round(self.screen_width / self.aspect_ratio)

    def _fit_image_to_screen(self, file_name):
        """Load, scale, and center an image to fit the screen exactly.

        Return the image object and its corresponding rect.

        It is up to the caller to blit and update the image after
        calling this method. Once that happens, there are no black bars
        anywhere around the image, and no stretching of it in any
        direction.
        """
        screen_width, screen_height = self._screen.get_size()
        screen_aspect_ratio = screen_width / screen_height

        image = _load_image(file_name, self.images_dir,
                            'a full-screen image')[0]
        image_width, image_height = image.get_size()
        image_aspect_ratio = image_width / image_height
        image.set_alpha(None, pygame.RLEACCEL)

        if image_width != screen_width or image_height != screen_height:
            if screen_aspect_ratio == image_aspect_ratio:
                image_size = (screen_width, screen_height)
            elif screen_aspect_ratio > image_aspect_ratio:
                image_size = (screen_width,
                              round(image_height * screen_width / image_width))
            else:
                image_size = (round(image_width *
                                    screen_height / image_height),
                              screen_height)

            try:
                image = pygame.transform.smoothscale(image, image_size)
            except ValueError:
                image = pygame.transform.scale(image, image_size)

        image_rect = image.get_rect()
        image_rect.center = self._screen_rect.center

        return image, image_rect

    def _display_splash_screen(self, screen):
        """Display a splash screen until a key, any key, is pressed."""
        image, img_rect = self._fit_image_to_screen(self.splash_image)

        screen.blit(image, img_rect)
        pygame.display.flip()

        # Detect if the player quit or if a key was pressed and released
        is_screen_done = False
        while not is_screen_done:
            for event in pygame.event.get():
                if self._has_quit(event):
                    self._handle_quit()
                    is_screen_done = True
                elif (event.type == pygame.KEYUP or
                      event.type == pygame.MOUSEBUTTONUP):
                    is_screen_done = True

    def _display_pause_message(self):
        """Print "Pause" on top of the game screen."""
        self._display_modal_text('Pause')
        self._is_pause_displayed = True

    def _display_modal_text(self, modal_text):
        """Display an important modal message centered on the screen."""
        text, text_rect = _get_rendered_text(self._modal_text_font, modal_text,
                                             self.font_color)
        text_rect.center = self._screen_rect.center

        # Display text shadow
        text_shadow = _get_rendered_text(self._modal_text_font, modal_text,
                                         MEDIUM_DARK_GRAY)[0]
        text_shadow_rect = text_rect.move(2, 2)

        self._screen.blit(text_shadow, text_shadow_rect)
        self._screen.blit(text, text_rect)
        pygame.display.update([text_shadow_rect, text_rect])

    def _handle_input(self, delta_time):
        """React to the player's input as necessary."""
        for event in pygame.event.get():
            if self._has_quit(event):
                self._handle_quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in self.keys_shoot and not self._is_paused:
                    self._player.shoot()
                    if len(self._missile_thumbnails) > 0:
                        self._thumbnail_group.remove(
                            self._missile_thumbnails.pop())
                elif event.key in self.keys_pause:
                    # Toggle paused state
                    self._is_paused = not self._is_paused
                    if self._is_pause_displayed:
                        self._is_pause_displayed = False
                elif event.key == pygame.K_F1:
                    self._is_screen_info_shown = not self._is_screen_info_shown
            elif (event.type == pygame.KEYUP and
                  event.key in self.keys_reload_ammo and
                  not self._is_paused):
                # Detect ammo reload when the reload key is released
                self._player.reload()

                # Update the ammo thumbs if not at max and not unlimited
                if (self._player.shots_left < self._player.MAX_SHOTS or
                    self._player.MAX_SHOTS > 0):
                    for i in range(len(self._missile_thumbnails)):
                        self._thumbnail_group.remove(
                            self._missile_thumbnails.pop())
                    self._create_thumbnails(self._missile_thumbnails,
                                            self.num_shots_pos, self.missile_image,
                                            self._player.shots_left)

        if self._is_paused:
            return

        # Detect left and right movement inputs
        self._keyboard_state = pygame.key.get_pressed()
        player_rect = self._player.rect

        self._player.is_moving_left = (
            self._is_key_active(self.keys_move_left) and player_rect.left > 0)

        self._player.is_moving_right = (
            self._is_key_active(self.keys_move_right) and
            player_rect.right < self._screen_rect.right)

        # Avoid moving to both left and right at the same time :O
        if self._player.is_moving_left and self._player.is_moving_right:
            self._player.is_moving_left = False
            self._player.is_moving_right = False

        # Update the player
        if self._player.is_moving_left or self._player.is_moving_right:
            self._player.update(delta_time)

    def _is_key_active(self, event_keys):
        """Return true if one the keys to a particular event is down."""
        num_keys = len(event_keys)
        for i in range(num_keys):
            if self._keyboard_state[event_keys[i]]:
                return True
        return False

    def _blit_current_score(self, has_changed):
        """Blit the player's current score to the screen."""
        if has_changed:
            score_text = ''.join(['Score: ', str(self._score)])
            self._score_text = self._screen_font.render(score_text, True,
                                                        self.font_color)
            self._score_rect = self._score_text.get_rect()
            self._score_rect.topleft = self.score_pos

        self._screen.blit(self._score_text, self.score_pos)

    def _blit_screen_info(self, fps):
        """Blit the screen resolution and current FPS to the screen.

        This method is not optimized for speed.
        """
        left_margin = 10
        bottom_offset = self._screen_rect.height - 70
        fps = str(round(fps, 1))
        fps_rect = self._blit_info_text(''.join(['FPS: ' + fps]),
                                        (left_margin, bottom_offset))

        bottom_offset = self._screen_rect.height - 40
        screen_res = ''.join([str(self._screen_rect.width), 'x',
                              str(self._screen_rect.height)])
        screen_res_rect = self._blit_info_text(''.join(['Screen size: ',
                                                        screen_res]),
                                               (left_margin, bottom_offset))
        return [fps_rect, screen_res_rect]

    def _blit_info_text(self, text, pos):
        """Blit text info to the screen and return the rect."""
        text_surf = self._screen_font.render(text, True, self.font_color)
        self._screen.blit(text_surf, pos)
        return text_surf.get_rect().move(pos)

    def _read_high_score(self):
        """Read the high score from the file.

        If the file doesn't exist yet, the high score is assumed to be
        0, and the file will be created later.
        """
        if os.path.isfile(self._data_file):
            with open(self._data_file, 'rb') as file:
                file_content = file.read(4)
                self._high_score = struct.unpack('I', file_content)[0]

    def _update_high_score(self):
        """Write the high score to the file."""
        self._high_score = self._score

        # Thanks to Blair Conrad at Stack Overflow for this algorithm
        # https://stackoverflow.com/questions/273192/how-can-i-create-a-
        # directory-if-it-does-not-exist
        if not os.path.exists(self._data_dir):
            try:
                os.makedirs(self._data_dir)
            except OSError as error:
                if error.errno != errno.EEXIST:
                    print(_ERR_PREFIX, "Couldn't create the", self._data_dir,
                          'folder to record the high score :(',
                          file=sys.stderr)
                    return

        with open(self._data_file, 'wb') as file:
            binary_score = struct.pack('I', self._high_score)
            file.write(binary_score)

    def _prompt_play_again(self):
        """Wait for the player to indicate if he wants to try again."""
        prompt_text = 'Press Enter to play again'
        prompt, prompt_rect = _get_rendered_text(self._screen_font,
                                                 prompt_text, self.font_color)
        prompt_rect.centerx = self._screen_rect.centerx
        prompt_rect.y = self._screen_rect.centery + 40
        self._screen.blit(prompt, prompt_rect)
        pygame.display.update(prompt_rect)

        # Wait for the keypress to play again
        is_waiting = True
        while is_waiting:
            for event in pygame.event.get():
                if self._has_quit(event):
                    self._handle_quit()
                    is_waiting = False
                elif (event.type == pygame.KEYDOWN and
                      (event.key == pygame.K_RETURN or
                       event.key == pygame.K_KP_ENTER)):
                    is_waiting = False

        self._is_main_loop_running = True

    def _has_quit(self, event):
        """Return true if the player has given an exit command."""
        # Check for the quit event, Esc key, or Alt+F4
        return (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and
                 (event.key == pygame.K_ESCAPE or
                  (event.key == pygame.K_F4 and
                   pygame.KMOD_ALT & pygame.key.get_mods()))))

    def _handle_quit(self):
        """Ask the player for confirmation before exiting the game."""
        with PolarDialogBox(self._screen, self._clock) as box:
            is_sure_quit = box.get_answer('Are you sure you want to quit?')

        if is_sure_quit:
            self._is_still_playing = False
            self._is_main_loop_running = False
            return

        if self._is_paused:
            self._is_paused = False

        if self._background_surf is not None:
            self._screen.blit(self._background_surf, (0, 0))
            pygame.display.flip()


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
        self.image, self.rect = _load_image(image_file, image_dir, 'the player')
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
            new_missile = Ammo(
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
        self.image, self.rect = _load_image(image_file, image_dir, 'the enemy')
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
        new_bomb = Ammo(
                self._bomb_data['group'],
                self._bomb_data['screen_rect'],
                self.rect.center,
                self._bomb_data['image_file'],
                self._bomb_data['image_dir'],
                not self._bomb_data['is_direction_up'],
                self._bomb_data['speed']
            )
        self._is_bomb_dropped = True


class Ammo(pygame.sprite.DirtySprite):
    """An object thrown at an opponent by someone in the game."""

    def __init__(self, group, screen_rect, initial_center_pos, image_file,
                 image_dir=None, is_direction_up=False, speed=800):
        """Set initial values for the ammo."""
        pygame.sprite.DirtySprite.__init__(self, group)
        self.image, self.rect = _load_image(image_file, image_dir, 'the ammo')
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


class GroundObject(pygame.sprite.Sprite):
    """An immobile ground structure to be defended by the player."""

    def __init__(self, group, pos, image_file,
                 razed_image_file=None, image_dir=None):
        """Initialize the ground object."""
        pygame.sprite.Sprite.__init__(self, group)
        self.image, self.rect = _load_image(image_file, image_dir,
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
                self.image = _load_image(self._razed_image_file,
                                         self._image_dir,
                                         'a razed ground object')[0]

class Thumbnail(pygame.sprite.Sprite):
    """A size-reduced representation of a sprite.

    The size of the resulting sprite is determined by the height
    specified. The image is resized to that height, preserving the aspect
    ratio and thus the relative width.
    """

    def __init__(self, group, pos, new_height, image_file, image_dir=None):
        """Initialize the thumbnail."""
        pygame.sprite.Sprite.__init__(self, group)
        self.image, image_rect = _load_image(image_file, image_dir,
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


class PolarDialogBox:
    """A modal dialog box to ask the user a yes-no ("polar") question.

    The answer can be selected by the user by clicking the appropriate
    button with the mouse, pressing the Y or N keys, or using the arrow
    keys to select a button and then pressing Enter. Escape kills the
    dialog box with no action taken.

    Instances of this class should be created using a 'with' statement.
    """
    YES_BUTTON = 0
    NO_BUTTON = 1

    def __init__(self, screen, clock, size=(400, 200)):
        """Initializes the values of the box."""
        self.size = size
        self.font_size = 28
        self.font_color_prompt = MEDIUM_DARK_GRAY
        self.font_color_buttons = WHITE
        self.background_color = LIGHT_GRAY
        self.border_color = GRAY
        self.button_color_default = GRAY
        self.border_width = 3
        self.shadow_x_offset = 3
        self.shadow_y_offset = 3
        self._screen = screen
        self._screen_rect = screen.get_rect()
        self._clock = clock
        self._font = pygame.font.Font(None, self.font_size)
        self._box_rect = None
        self._button_yes_rect = None
        self._button_no_rect = None
        self._button_ctr_offset = 20
        self._focused_button = self.YES_BUTTON
        self._active_button = None

        if (pygame.event.get_blocked(pygame.KEYDOWN) or
            pygame.event.get_blocked(pygame.MOUSEMOTION) or
            pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN) or
            pygame.event.get_blocked(pygame.MOUSEBUTTONUP)):
            pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEMOTION,
                                      pygame.MOUSEBUTTONDOWN,
                                      pygame.MOUSEBUTTONUP])

        pygame.mouse.set_visible(True)

    def __enter__(self):
        """Return the box instance upon entering."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Remove the mouse cursor on window exit."""
        pygame.mouse.set_visible(False)

    def get_answer(self, prompt_text):
        """Display the dialog box and wait for the user's response.

        The return value is true if the answer is yes, false otherwise.
        """
        self._render_box(prompt_text)

        while True:
            self._render_buttons()
            is_answer_yes = self._get_input()

            if is_answer_yes is not None:
                return is_answer_yes

            if self._clock is not None:
                self._clock.tick(60)

    def _render_box(self, prompt_text):
        """Draw the dialog box centered on the screen."""
        box, box_rect = _get_surface(self.size, self.background_color)

        # Blit the prompt text onto the box
        prompt, prompt_rect = _get_rendered_text(self._font,
                                                 prompt_text,
                                                 self.font_color_prompt)
        prompt_rect.centerx = box_rect.centerx
        prompt_rect.y = box_rect.height * 0.25
        box.blit(prompt, prompt_rect)

        # Draw the border
        if self.border_width > 0:
            pygame.draw.rect(box, self.border_color,
                             box_rect, self.border_width)

        # Center the box and give the rect to the instance
        box_rect.center = self._screen_rect.center
        self._box_rect = box_rect

        # Make the box shadow
        box_shadow = box.copy()
        box_shadow.fill(MEDIUM_DARK_GRAY)
        box_shadow_rect = box_rect.move(self.shadow_x_offset,
                                        self.shadow_y_offset)

        # Put the box on the screen
        self._screen.blit(box_shadow, box_shadow_rect)
        self._screen.blit(box, box_rect)
        pygame.display.update([box_shadow_rect, box_rect])

    def _render_buttons(self):
        """Draw the Yes and No buttons in their current state."""
        button_yes, button_yes_rect = self._get_button('Yes', self.YES_BUTTON)
        button_no, button_no_rect = self._get_button('No', self.NO_BUTTON)

        if self._button_yes_rect is None or self._button_no_rect is None:
            self._button_yes_rect = button_yes_rect
            self._button_no_rect = button_no_rect

        self._screen.blit(button_yes, button_yes_rect)
        self._screen.blit(button_no, button_no_rect)
        pygame.display.update([button_yes_rect, button_no_rect])

    def _get_button(self, text, button_specifier):
        """Return a button surface containing the text."""
        size = (90, 40)

        if button_specifier == self._active_button:
            # Invert the colors when active
            background_color = self.font_color_buttons
            text_color = self.button_color_default
        else:
            background_color = self.button_color_default
            text_color = self.font_color_buttons

        button, button_rect = _get_surface(size, background_color)
        text, text_rect = _get_rendered_text(self._font, text, text_color)
        _blit_text_to_surface(text, button, text_rect, button_rect)

        # Draw the border if this button has the focus
        if button_specifier == self._focused_button:
            pygame.draw.rect(button, BLACK, button_rect, self.border_width)

        # Position the button in the right place
        if button_specifier == self.YES_BUTTON:
            button_rect.right = (self._box_rect.centerx
                                 - self._button_ctr_offset)
        else:
            button_rect.left = self._box_rect.centerx + self._button_ctr_offset

        button_rect.y = self._box_rect.centery + self._button_ctr_offset

        return (button, button_rect)

    def _get_input(self):
        """Return true if the user answers yes, false otherwise.

        If the input doesn't correspond to a final answer, such as
        moving focus from one button to another, then the return value
        is None.
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self._focused_button = self.YES_BUTTON
                    self._active_button = self.YES_BUTTON
                    return True
                elif event.key == pygame.K_n:
                    self._focused_button = self.NO_BUTTON
                    self._active_button = self.NO_BUTTON
                    return False
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif (event.key == pygame.K_RETURN or
                      event.key == pygame.K_KP_ENTER):
                    if self._focused_button == self.YES_BUTTON:
                        self._active_button = self.YES_BUTTON
                        return True
                    self._active_button = self.NO_BUTTON
                    return False
                elif (event.key == pygame.K_LEFT and
                      self._focused_button == self.NO_BUTTON):
                    self._focused_button = self.YES_BUTTON
                elif (event.key == pygame.K_RIGHT and
                      self._focused_button == self.YES_BUTTON):
                    self._focused_button = self.NO_BUTTON
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if self._button_yes_rect.collidepoint(mouse_pos):
                    self._focused_button = self.YES_BUTTON
                elif self._button_no_rect.collidepoint(mouse_pos):
                    self._focused_button = self.NO_BUTTON
                elif self._active_button is not None:
                    self._active_button = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self._button_yes_rect.collidepoint(mouse_pos):
                    self._active_button = self.YES_BUTTON
                elif self._button_no_rect.collidepoint(mouse_pos):
                    self._active_button = self.NO_BUTTON
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self._button_yes_rect.collidepoint(mouse_pos):
                    return True
                elif self._button_no_rect.collidepoint(mouse_pos):
                    return False
        return None


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
    square, square_rect = _get_surface((64, 64), RED)
    font = pygame.font.Font(None, 72)
    text, text_rect = _get_rendered_text(font, '?', WHITE)
    _blit_text_to_surface(text, square, text_rect, square_rect)
    return square
