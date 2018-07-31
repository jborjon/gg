#!/usr/bin/env python3

import gg

# Main function definition
def main():
    """Main function."""
    game = gg.Game()

    # Set the attributes of the game to make it your own
    game.name = "Mr. Borjon's Most Awesomest Gamest: Flak"
    game.images_dir = 'example_pics'
    game.splash_image = 'splash.bmp'
    game.player_image = 'guy.gif'
    game.enemy_image = 'face.gif'
    game.missile_image = 'ray.png'
    game.bomb_image = 'bomb.png'
    game.building_image = 'building.png'
    game.building_razed_image = 'building_razed.png'
    game.background_image = 'mountains.bmp'
    game.window_icon = 'ball.png'
    game.player_num_shots = 10
    game.is_fullscreen = True

    # Run the game
    game.run()

# Call main() to start the program
if __name__ == '__main__':
    main()
