import arcade

import game_view


class InstructionView(arcade.View):
    """ View to show instructions """

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Space Invaders", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to Start", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        my_game_view = game_view.GameView()
        my_game_view.setup()
        self.window.show_view(my_game_view)
