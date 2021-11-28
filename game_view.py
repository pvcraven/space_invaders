import random
import arcade
from pyglet.math import Vec2

from enemy_bullet import EnemyBullet
from constants import *
from enemy_invader import EnemyInvader
import instruction_view


class GameView(arcade.View):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.shield_list = None

        # Textures for the enemy
        self.enemy_textures = None

        # State of the game
        self.game_state = PLAY_GAME

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.lives = 3
        self.death_pause = 0

        self.filter_on = True

        # Enemy movement
        self.enemy_change_x = -ENEMY_SPEED

        # Create the crt filter
        self.crt_filter = arcade.experimental.CRTFilter(SCREEN_WIDTH, SCREEN_HEIGHT,
                                                        resolution_down_scale=5.0,
                                                        hard_scan=-8.0,
                                                        hard_pix=-3.0,
                                                        display_warp= Vec2(1.0 / 32.0, 1.0 / 24.0),
                                                        mask_dark=0.5,
                                                        mask_light=1.5)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        self.player_explosion = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover4.wav")

        arcade.set_background_color(arcade.color.BLACK)

        # arcade.configure_logging()

    def setup_level_one(self):
        # Load the textures for the enemies, one facing left, one right
        # Create rows and columns of enemies
        column_count = 10
        x_start = 380
        x_spacing = 90

        row_count = 5
        y_start = 720
        y_spacing = 60
        for column in range(column_count):
            x = x_start + x_spacing * column
            for row in range(row_count):
                y = y_start + y_spacing * row
                score = 0

                if row == 0 or row == 1:
                    texture1 = arcade.load_texture("images/sprite_05.png")
                    texture2 = arcade.load_texture("images/sprite_06.png")
                    score = 10
                elif row == 2 or row == 3:
                    texture1 = arcade.load_texture("images/sprite_01.png")
                    texture2 = arcade.load_texture("images/sprite_02.png")
                    score = 20
                else:
                    texture1 = arcade.load_texture("images/sprite_03.png")
                    texture2 = arcade.load_texture("images/sprite_04.png")
                    score = 30

                # Create the enemy instance
                # enemy image from kenney.nl
                enemy = EnemyInvader(texture1, texture2)
                enemy.score = score
                enemy.scale = SPRITE_SCALING_enemy

                # Position the enemy
                enemy.center_x = x
                enemy.center_y = y

                # Add the enemy to the lists
                self.enemy_list.append(enemy)

    def make_shield(self, x_start):
        """
        Make a shield, which is just a 2D grid of solid color sprites
        stuck together with no margin so you can't tell them apart.
        """
        shield_block_width = 5
        shield_block_height = 10
        shield_width_count = 25
        shield_height_count = 7
        y_start = 170
        for x in range(x_start,
                       x_start + shield_width_count * shield_block_width,
                       shield_block_width):
            for y in range(y_start,
                           y_start + shield_height_count * shield_block_height,
                           shield_block_height):
                shield_sprite = arcade.SpriteSolidColor(shield_block_width,
                                                        shield_block_height,
                                                        arcade.color.WHITE)
                shield_sprite.center_x = x
                shield_sprite.center_y = y
                self.shield_list.append(shield_sprite)

    def setup(self):
        """
        Set up the game and initialize the variables.
        Call this method if you implement a 'play again' feature.
        """

        self.game_state = PLAY_GAME

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.shield_list = arcade.SpriteList(is_static=True)

        # Set up the player
        self.score = 0

        # Image from kenney.nl
        self.player_sprite = arcade.Sprite("images/player.png",
                                           SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 60
        self.player_sprite.color = PLAYER_COLOR
        self.player_list.append(self.player_sprite)

        # Make each of the shields
        for x in range(140, 1200, 270):
            self.make_shield(x)

        self.setup_level_one()

    def draw(self):
        # Draw all the sprites.
        self.enemy_list.draw(pixelated=True)
        self.player_bullet_list.draw(pixelated=True)
        self.enemy_bullet_list.draw(pixelated=True)
        self.shield_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

        # Render the text
        arcade.draw_text(f"Score: {self.score:04}",
                         start_x=30,
                         start_y=SCREEN_HEIGHT - 35,
                         color=arcade.color.WHITE,
                         font_size=24,
                         font_name="Kenney Rocket")

        # Render the text
        arcade.draw_text(f"Lives: {self.lives}",
                         start_x=SCREEN_WIDTH - 300,
                         start_y=SCREEN_HEIGHT - 35,
                         color=arcade.color.WHITE,
                         font_size=24,
                         align="right",
                         width=300,
                         font_name="Kenney Rocket")

        # Draw game over if the game state is such
        if self.game_state == GAME_OVER:
            arcade.draw_text(text="GAME OVER",
                             start_x=0,
                             start_y=SCREEN_HEIGHT / 2 + 20,
                             color=arcade.color.RED,
                             font_size=65,
                             width=SCREEN_WIDTH,
                             align="center",
                             font_name="Kenney Rocket")

            arcade.draw_text(text="Press Space",
                             start_x=0,
                             start_y=SCREEN_HEIGHT / 2 - 35,
                             color=arcade.color.RED,
                             font_size=35,
                             width=SCREEN_WIDTH,
                             align="center",
                             font_name="Kenney Rocket")

            self.window.set_mouse_visible(True)

    def on_draw(self):
        """ Render the screen. """

        if self.filter_on:
            # Draw our stuff into the CRT filter
            self.crt_filter.use()
            self.crt_filter.clear()
            self.draw()

            # Switch back to our window and draw the CRT filter do
            # draw its stuff to the screen
            self.window.use()
            self.window.clear()

            self.crt_filter.draw()
        else:
            # Draw our stuff into the screen
            self.window.use()
            self.window.clear()
            self.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called whenever the mouse moves. """

        # Don't move the player if the game is over
        if self.game_state == GAME_OVER:
            return

        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        if self.death_pause:
            return

        # Only allow the user so many bullets on screen at a time to prevent
        # them from spamming bullets.
        if len(self.player_bullet_list) < MAX_PLAYER_BULLETS:

            # Gunshot sound
            arcade.play_sound(self.gun_sound)

            # Create a bullet
            bullet = arcade.Sprite("images/player_bullet.png", SPRITE_SCALING_LASER)
            bullet.color = PLAYER_COLOR

            # Give the bullet a speed
            bullet.change_y = PLAYER_BULLET_SPEED

            # Position the bullet
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            # Add the bullet to the appropriate lists
            self.player_bullet_list.append(bullet)

    def update_enemies(self):

        # Move the enemy vertically
        for enemy in self.enemy_list:
            enemy.center_x += self.enemy_change_x

        # Check every enemy to see if any hit the edge. If so, reverse the
        # direction and flag to move down.
        move_down = False
        for enemy in self.enemy_list:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                move_down = True
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True

        # Did we hit the edge above, and need to move the enemy down?
        if move_down:
            # Yes
            for enemy in self.enemy_list:
                # Move enemy down
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT

    def allow_enemies_to_fire(self):
        """
        See if any enemies will fire this frame.
        """
        # Track which x values have had a chance to fire a bullet.
        # Since enemy list is build from the bottom up, we can use
        # this to only allow the bottom row to fire.
        x_spawn = []
        for enemy in self.enemy_list:
            if enemy.dead:
                continue

            # Adjust the chance depending on the number of enemies. Fewer
            # enemies, more likely to fire.
            chance = 3 + len(self.enemy_list) * 20

            # Fire if we roll a zero, and no one else in this column has had
            # a chance to fire.
            if random.randrange(chance) == 0 and enemy.center_x not in x_spawn:
                # Create a bullet
                bullet = EnemyBullet()

                # Give the bullet a speed
                bullet.change_y = -BULLET_SPEED

                # Position the bullet so its top id right below the enemy
                bullet.center_x = enemy.center_x
                bullet.top = enemy.bottom

                # Add the bullet to the appropriate list
                self.enemy_bullet_list.append(bullet)

            # Ok, this column has had a chance to fire. Add to list so we don't
            # try it again this frame.
            x_spawn.append(enemy.center_x)

    def process_enemy_bullets(self):

        # Move the bullets
        self.enemy_bullet_list.update()

        # Loop through each bullet
        for bullet in self.enemy_bullet_list:
            # Check this bullet to see if it hit a shield
            hit_list = arcade.check_for_collision_with_list(bullet, self.shield_list)

            # If it did, get rid of the bullet and shield blocks
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            # See if the player got hit with a bullet
            if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list):
                if self.lives > 0:
                    arcade.play_sound(self.player_explosion)
                    self.lives -= 1
                    self.enemy_bullet_list = arcade.SpriteList()
                    self.player_bullet_list = arcade.SpriteList()
                    self.death_pause = DEATH_PAUSE_TIME
                else:
                    self.game_state = GAME_OVER
                    arcade.play_sound(self.game_over)

            # If the bullet falls off the screen get rid of it
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def process_player_bullets(self):

        # Move the bullets
        self.player_bullet_list.update()

        # Loop through each bullet
        for bullet in self.player_bullet_list:

            # Check this bullet to see if it hit a shield
            hit_list = arcade.check_for_collision_with_list(bullet, self.shield_list)
            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            # Check this bullet to see if it hit a enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # For every enemy we hit, add to the score and remove the enemy
            for enemy in hit_list:
                if enemy.dead:
                    continue
                bullet.remove_from_sprite_lists()
                enemy.explode()

                self.score += enemy.score

                # Hit Sound
                arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):
        """ Movement and game logic """

        if self.death_pause > 0:
            self.death_pause -= delta_time
            if self.death_pause < 0:
                self.death_pause = 0
            return

        self.enemy_bullet_list.on_update(delta_time)
        self.enemy_list.on_update(delta_time)

        if self.game_state == GAME_OVER:
            return

        self.update_enemies()
        self.allow_enemies_to_fire()
        self.process_enemy_bullets()
        self.process_player_bullets()

        if len(self.enemy_list) == 0:
            self.setup_level_one()

    def on_key_press(self, symbol: int, modifiers: int):
        if self.game_state == GAME_OVER and symbol == arcade.key.SPACE:
            my_game_view = instruction_view.InstructionView()
            self.window.show_view(my_game_view)
