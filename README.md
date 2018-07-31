# GameGenerator

GameGenerator (GG) is a simple 2D game engine for creating Flak games. It amounts to a complete, customizable game environment for making Flak-style 2D games.


## What's a Flak game?

Flak, the style of game supported by GG, consists of a player on the ground (the bottom of the screen) attempting to shoot down enemy planes performing their bombing runs. The player and the ground structures the player defends must survive, with the player reloading every few shots when out of ammo (with unlimited reloads). It's fast-paced, challenging, and exciting!

The player gets a number of points for hitting enemies and bombs, and loses points when ground structures are destroyed by bombs. There is an unlimited number of enemy planes, who will continue to spawn as long as the game is running. Once all the buildings are destroyed or the player has lost all her lives, the game is over. The only way to win? Beat the high score.

In case you're itching to know: Flak is short for *Flugzeugabwehrkanone* (say it fast 10 times), which is German for "aircraft defense cannon." Anti-aircraft artillery. This stuff:

![Flak being fired](https://upload.wikimedia.org/wikipedia/commons/1/13/Antiaircraft_defence_Sweden_1934.jpg)


## Getting Started

### Prerequisites

You need to have [Python 3.x](https://www.python.org/downloads) and [Pygame](https://www.pygame.org/wiki/GettingStarted) installed in your machine in order to run GameGenerator and the games created with it.


### Installing

The `gg` folder contains the full GameGenerator package; you might say it *is* the package. Copy that folder to your own game folder, or put it somewhere else and [add it to the Python path](https://www.digitalocean.com/community/tutorials/how-to-write-modules-in-python-3) using `sys.path.append(full_path_to_folder_containing_gg)` from the Python Shell.

**Note to Madison Middle School students:** As of July 31, 2018, each Raspberry Pi in the Young Engineers classroom has a copy of `gg` in the `Documents` folder. Simply copy and paste the `gg` folder into your own folder to create games.


### Example game

The `flak_example.py` file contains a full working game. Okay, not a very good one, but one you can still use for reference. The background and splash screen images were created using Scratch.


### Creating your first game

#### Images

For your game to look like a game, it needs images. These images are used to dress up the sprites (that is, the characters and objects) and backgrounds in your game. For testing purposes, you can simply draw colored circles, squares, or lines.

Using any drawing program that can save images, create a separate file for each of the following items:

  * The player

  * The enemy (a single enemy image will be applied to all the enemies, so you only need to draw it once)

  * The missile fired by the player

  * A bomb dropped by the enemy

  * A ground building

There are also optional images you can draw, with no consequences if you don't:

  * The background (try to get the size in pixels as close as possible to the way you want it in the game)

  * A destroyed building to display when a building gets hit

  * A splash screen, possibly with your logo and credits, displayed before the game starts

Save your images with a descriptive file name in the same folder as your game code or, as I would recommend, in its own subfolder within the game folder.

GG can handle PNG, JPG, GIF, and all other [image formats supported by Pygame](https://www.pygame.org/docs/ref/image.html). Make sure the sprite images are not so big that they cover the entire screen or make the game unplayable.

**Note to Madison students:** Although I haven't found any good free Raspberry Pi software for creating images, you can use [Scratch](https://scratch.mit.edu) to draw sprites and backgrounds and then export them as images; or you can create images in a different computer and then bring them to class in a USB drive.


#### Programming

After putting the `gg` folder in the location of your choice, create a new `.py` file (you could call it `flak.py`, for example) and import the GG package:

```python
import gg
```

Then create a variable to contain the game. For simplicity, let's call it `game`:

```python
game = gg.Game()
```

This variable contains your entire game environment: the player, enemies, images, ammo, etc.

Next, customize your game at will by modifying the **attributes** of `game` you wish to customize using the `variable_name.attribute_name = attribute_value` syntax (notice the period or dot), often called "dot notation":

```python
game.name = 'My Shiny Flak Game'
game.player_image = 'good-guy.png'
game.enemy_image = 'bad-guy.png'
game.player_num_shots = 10
game.is_fullscreen = True
```

All attributes other than image files come with useful defaults, so you don't *have* to set any non-image attributes, but it's way more fun if you make the game your very own.

Okay, images do have defaults: if you don't specify an image file for a certain character, the file you specify doesn't exist, or the image specified can't be loaded for any reason, the missing image will be replaced by the Red Square of Doom, a red square with a white question mark inside. In spite of its ominous name, the RSOD is very useful: it makes it obvious to you that an image is missing and shows you where, saving you some guesswork.

The exception to the RSOD is the game background. If you don't specify a file, you get a solid-black background.

Once you're finished customizing your game, run it:

```python
game.run()
```

That's it! When you run your Python game file, your game should start.


## Full attribute list

The following are all the attributes you can modify to make the game your own. You'll see that you are not limited to making a game in the way I described under "What's a Flak game?" Be creative and break boundaries.

| Attribute | Description | Type | Default value |
| --- | --- | --- | --- |
| `name` | The name of the game, displayed on the window title bar, if there is one. | String | `'GG Flak'` |
| `images_dir` | The name of the directory where the images are. | String | `None` |

  * `images_dir`: the name of the directory where the images are. Default: `None`.

  * `window_icon`: file name of the icon to display next to the name. Default: `None`.

  * `splash_image`: the image that covers the screen at the beginning. Default: `None`.

  * `screen_width`: the window width in pixels if not fullscreen. Default: `800`.

  * `aspect_ratio`: the aspect ratio of the window if not fullscreen. Default: `1.7778`.

  * `is_fullscreen`: whether the window covers the entire screen. Default: `False`.

  * `font_color`: the color of the text that appears on the screen. Default: `gg.colors.WHITE`.

  * `screen_font_size`: the point size of the info text on the screen. Default: `36`.

  * `background_color`: a solid color used if no image is specified. Default: `gg.colors.BLACK`.

  * `background_image`: file name of the image to put as background. Default: `None`.

  * `player_image`: the image file for the player object. Default: `None`.

  * `player_num_lives`: number of tries the player gets before losing. Default: `3`.

  * `player_num_shots`: number of shots per reload. 0 means no reloading. Default: `10`.

  * `player_speed`: how far the player moves left or right in one second. Default: `800`.

  * `player_x_pos`: the initial x-coordinate of the player's top left. Default: ``.

  * `player_y_pos`: the initial y-coordinate of the player's top left. Default: ``.

  * `has_player_sprite_dir`: flip the player sprite when moving? Default: ``.

  * `missile_image`: the image file for the missile fired by the player. Default: ``.

  * `missile_speed`: how fast the player missile travels. Default: ``.

  * `is_missile_upward`: does the missile move upward? Down otherwise. Default: ``.

  * `enemy_image`: the image for all the enemy objects. Default: ``.

  * `enemy_speed`: how fast the enemy airplanes move. Default: ``.

  * `enemy_count`: max number of enemies on the screen at any given time. Default: ``.

  * `enemy_top_edge`: top of the boundary where enemies can spawn. Default: ``.

  * `enemy_bottom_edge`: bottom of the boundary where enemies can spawn. Default: ``.

  * `bomb_image`: the image file for the bomb dropped by the enemy. Default: ``.

  * `bomb_speed`: how fast the enemy bombs travel. Default: ``.

  * `is_bomb_downward`: does the bomb move downward? Up otherwise. Default: ``.

  * `building_image`: the image file for the ground structure objects. Default: ``.

  * `building_razed_image`: optional image for buildings that are hit. Default: ``.

  * `building_count`: how many buildings to have on the screen. Must be > 1 Default: ``.

  * `score_pos`: the position where the score is displayed on the screen. Default: ``.

  * `score_factor`: how many points the player gets per hit. Default: ``.

  * `score_loss_factor`: points lost when a building is razed. Default: ``.

  * `high_score_pos`: the position where the high score is displayed. Default: ``.

  * `num_lives_pos`: the location of the player's remaining lives panel. Default: ``.

  * `num_shots_pos`: the location of the player's remaining shots panel. Default: ``.

  * `thumbnails_height`: the height of the lives and shots thumbnails. Default: ``.

  * `message_high_score`: message to show when the player gets highscore. Default: ``.

  * `message_game_over`: message to show when the player loses. Default: ``.

  * `keys_move_left`: list of keys that move the player left. Default: ``.

  * `keys_move_right`: list of keys that move the player right. Default: ``.

  * `keys_shoot`: list of keys that fire the missile. Default: ``.

  * `keys_reload_ammo`: list of keys that reload the ammo when out. Default: ``.

  * `keys_pause`: list of keys that pause the game. Default: ``.

There is a single method (function) you can call:

  * `run()`: once all the modifiable attributes are set as desired, call this method to start the game.


## Author

Mr. [Joseph Borjon](https://www.linkedin.com/in/josephborjon), Young Engineers teacher at Madison Middle School.


## License

You may modify and redistribute this project under certain restrictions; see the [LICENSE](LICENSE.md) file for complete details.


## Contributing

If you make any changes or improvements to any part of this code, I'd love to know about it. We may even add it to the main branch. Please contact me via [LinkedIn](https://www.linkedin.com/in/josephborjon) or email at work@josephborjon.com.


## Special thanks

A shout out to all my Young Engineers students at Madison Middle School in [Rexburg, Idaho](https://en.wikipedia.org/wiki/Rexburg,_Idaho), during the 2016-2017 and 2017-2018 school years for inspiring me to spend countless unpaid hours for about 4 grueling weeks in order to create this software. It was a labor of love. Yoou guys are the best!
