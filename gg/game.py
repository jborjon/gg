# game.py
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
import struct
import gg.colors
import gg.utils

try:
    import pygame
except ImportError as err:
    print(gg.utils._ERR_PREFIX, err, ':_( Terminating game.', file=sys.stderr)
    sys.exit(1)


class Game:
    """The entire environment for creating and playing a Flak game.

    The client (you) should set his or her own values for the game
    attributes, but they are set up by default so that everything except
    images works out of the box.

    Modifiable attributes:

    -name: the name of the game, displayed on the window title bar.
    -images_dir: the path of the directory where the images are.
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
    -is_missile_upward: does the missile move up or down? Up if true.
    -enemy_image: the image for all the enemy objects.
    -enemy_speed: how fast the enemy airplanes move.
    -enemy_count: max number of enemies on the screen at any given time.
    -enemy_top_edge: top of the boundary where enemies can spawn.
    -enemy_bottom_edge: bottom of the boundary where enemies can spawn.
    -bomb_image: the image file for the bomb dropped by the enemy.
    -bomb_speed: how fast the enemy bombs travel.
    -is_bomb_downward: does the bomb move down or up? Down if true.
    -building_image: the image file for the ground structure objects.
    -building_razed_image: optional image for buildings that are hit.
    -building_count: how many buildings to start game with. Must be > 1.
    -building_y_pos: y-coordinate of buildings; None means near bottom.
    -score_pos: the position where the score is displayed on the screen.
    -score_factor: how many points the player gets per hit.
    -score_loss_factor: points lost when a building is destroyed.
    -high_score_pos: where to display highscore; None means top-center.
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
        self.font_color = gg.colors.WHITE
        self.screen_font_size = 36
        self.background_color = gg.colors.BLACK
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
        self._background_surf = gg.utils._get_surface(
            self._screen.get_size())[0]
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

        self._player = gg.player.Player(missile_data, self._screen_rect,
                                        self.player_image, self.images_dir,
                                        self.player_x_pos, self.player_y_pos,
                                        self.player_speed,
                                        self.player_num_lives,
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
            gg.enemy.Enemy(self._enemy_group, bomb_data, self._screen_rect,
                           enemy_boundaries, self.enemy_image, self.images_dir,
                           self.enemy_speed)

        # Place the buildings at regular intervals
        building_rect = gg.utils._load_image(self.building_image,
                                             self.images_dir,
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

            gg.groundobject.GroundObject(self._building_group, building_pos,
                                         self.building_image,
                                         self.building_razed_image,
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

            last_thumbnail = gg.thumbnail.Thumbnail(self._thumbnail_group,
                                                    thumbnail_pos,
                                                    self.thumbnails_height,
                                                    image_file,
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
            print(gg.utils._ERR_PREFIX, "Couldn't load the icon",
                  path, file=sys.stderr)

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

        image = gg.utils._load_image(file_name, self.images_dir,
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
        text, text_rect = gg.utils._get_rendered_text(self._modal_text_font,
                                                      modal_text,
                                                      self.font_color)
        text_rect.center = self._screen_rect.center

        # Display text shadow
        text_shadow = gg.utils._get_rendered_text(
            self._modal_text_font, modal_text, gg.colors.MEDIUM_DARK_GRAY)[0]
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
        prompt, prompt_rect = gg.utils._get_rendered_text(self._screen_font,
                                                          prompt_text,
                                                          self.font_color)
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
        with gg.polardialogbox.PolarDialogBox(self._screen, self._clock)\
             as box:
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
