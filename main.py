# Imports
import arcade
import random
from sprites.paddle import Paddle
from sprites.ball import Ball
import os

# CONSTANTS
# Screen dimensions and title
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Pong Game"

# Scaling factor for sprites
SCALING = 0.5

# Get the directory path for resource loading
DIR_PATH = os.path.dirname(os.path.abspath(__file__))

class Pong(arcade.Window):
  """Main application class for the Pong game."""
  
  def __init__(self, width, height, title):
    # Call the parent class initializer
    super().__init__(width, height, title)

    # Set up the empty sprite lists
    self.paddles_list = arcade.SpriteList()
    self.all_sprites = arcade.SpriteList()
    self.paused = False
    self.started = False
    self.mode = 2  # default to 2 player mode

    # initialize the font for scoring display
    self.score_font = arcade.load_font(f"{DIR_PATH}/fonts/square_sans_serif_7.ttf")

  def setup(self):
    # Set the background color
    arcade.set_background_color(arcade.color.BLACK)

    # Set up the paddles and place them in the middle of the screen
    # on the left and right sides
    self.player1 = Paddle(f"{DIR_PATH}/images/paddle.png", SCALING)
    self.player1.center_y = self.height / 2
    self.player1.left = 15
    # Add paddles to sprite lists
    self.paddles_list.append(self.player1)
    self.all_sprites.append(self.player1)
    
    self.player2 = Paddle(f"{DIR_PATH}/images/paddle.png", SCALING)
    self.player2.center_y = self.height / 2
    self.player2.right = self.width - 15
    # Add paddles to sprite lists
    self.paddles_list.append(self.player2)
    self.all_sprites.append(self.player2)

    # Set up the ball and place it in the center of the screen
    self.ball_sprite = Ball(f"{DIR_PATH}/images/ball.png", SCALING, DIR_PATH)
    self.ball_sprite.center_x = self.width / 2
    self.ball_sprite.center_y = self.height / 2
    # Add ball to sprite list
    self.all_sprites.append(self.ball_sprite)

    # Set up the text display for scores
    self.player1_score_text = arcade.Text(
      text="0",
      x=SCREEN_WIDTH / 2 - 15,
      y=SCREEN_HEIGHT - 30,
      color=arcade.color.WHITE,
      font_size=20,
      # I used a custom font to match the retro style of Pong
      font_name="Square Sans Serif 7",
      anchor_x="right",
      anchor_y="top"
    )

    self.player2_score_text = arcade.Text(
      text="0",
      x=SCREEN_WIDTH / 2 + 15,
      y=SCREEN_HEIGHT - 30,
      color=arcade.color.WHITE,
      font_size=20,
      font_name="Square Sans Serif 7",
      anchor_x="left",
      anchor_y="top"
    )

    # Set up text for choosing 1 player or 2 player mode
    # in the top left corner
    self.mode_text = arcade.Text(
      text="2 Player Mode",
      x=15,
      y=SCREEN_HEIGHT - 15,
      color=arcade.color.WHITE,
      font_size=16,
      anchor_x="left",
      anchor_y="top"
    )

    self.switch_mode_text = arcade.Text(
      text="Press Tab to switch to 1 Player Mode",
      x=15,
      y=SCREEN_HEIGHT - 40,
      color=arcade.color.WHITE,
      font_size=16,
      anchor_x="left",
      anchor_y="top"
    )

    # Set up text for starting, pausing, and quiting the game
    # in the top right corner
    self.pause_text = arcade.Text(
      text="Press P to Pause/Unpause",
      x=SCREEN_WIDTH - 15,
      y=SCREEN_HEIGHT - 15,
      color=arcade.color.WHITE,
      font_size=16,
      anchor_x="right",
      anchor_y="top"
    )
    self.start_text = arcade.Text(
      text="Press Space to Start",
      x=SCREEN_WIDTH - 15,
      y=SCREEN_HEIGHT - 40,
      color=arcade.color.WHITE,
      font_size=16,
      anchor_x="right",
      anchor_y="top"
    )
    self.exit_text = arcade.Text(
      text="Press Esc to Quit",
      x=SCREEN_WIDTH - 15,
      y=SCREEN_HEIGHT - 65,
      color=arcade.color.WHITE,
      font_size=16,
      anchor_x="right",
      anchor_y="top"
    )

    # Set up sounds
    self.hit_paddle_sound = arcade.load_sound(f"{DIR_PATH}/sounds/hit_paddle.wav")
    self.score_sound = arcade.load_sound(f"{DIR_PATH}/sounds/score.wav")

  def on_draw(self):
    """Render the screen."""
    # Start the render process by clearing the screen
    # and drawing all sprites
    self.clear()
    self.all_sprites.draw()

    # Draw the score texts
    self.player1_score_text.draw()
    self.player2_score_text.draw()

    # Draw the mode and control texts only if the game hasn't started
    if self.started == False:
      self.mode_text.draw()
      self.switch_mode_text.draw()
      self.start_text.draw()
      self.pause_text.draw()
      self.exit_text.draw()


  def on_update(self, delta_time: float):
    """All the game logic goes here.
    Collisions, scoring, and AI movement is included here."""

    # Skip updates if the game is paused
    if self.paused:
      return
    
    # Check for collisions between ball and player1 paddle
    if self.player1.collides_with_sprite(self.ball_sprite):
        # If a collision is detected, play sound and
        # adjust ball movement
        arcade.play_sound(self.hit_paddle_sound)
        self.set_bounce_angle(self.player1)
        self.ball_sprite.move_right()

    # Check for collisions between ball and player2 paddle
    if self.player2.collides_with_sprite(self.ball_sprite):
        # If a collision is detected, play sound and
        # adjust ball movement
        arcade.play_sound(self.hit_paddle_sound)
        self.set_bounce_angle(self.player2)
        self.ball_sprite.move_left()

    # If the ball goes past the left edge,
    # player 2 scores
    if self.ball_sprite.left < 0:
      arcade.play_sound(self.score_sound)
      self.ball_sprite.stop_moving()
      self.started = False
      self.ball_sprite.center_x = self.width / 2
      self.ball_sprite.center_y = self.height / 2
      self.player2_score_text.text = str(int(self.player2_score_text.text) + 1)

    # If the ball goes past the right edge,
    # player 1 scores
    if self.ball_sprite.right > self.width:
      arcade.play_sound(self.score_sound)
      self.ball_sprite.stop_moving()
      self.started = False
      self.ball_sprite.center_x = self.width / 2
      self.ball_sprite.center_y = self.height / 2
      self.player1_score_text.text = str(int(self.player1_score_text.text) + 1)

    # Simple AI for player 2 paddle in 1 player mode
    if self.mode == 1:
      # Keep the paddle centered on the ball by comparing
      # the y positions of the ball and paddle
      if self.ball_sprite.center_y > self.player2.center_y + 10:
        self.player2.up_pressed = True
        self.player2.down_pressed = False
      elif self.ball_sprite.center_y < self.player2.center_y - 10:
        self.player2.up_pressed = False
        self.player2.down_pressed = True
      else:
        self.player2.up_pressed = False
        self.player2.down_pressed = False
      self.player2.set_speed()
    
    # Update all sprites
    self.all_sprites.update(delta_time)

  def on_key_press(self, key, modifiers):
    # Pause control
    if key == arcade.key.P:
      self.paused = not self.paused

    # Exit control
    if key == arcade.key.ESCAPE:
      arcade.close_window()

    # Player controls are different than default arcade
    # to allow for smoother movement
    # Player 1 controls
    if key == arcade.key.W:
      self.player1.up_pressed = True
      self.player1.set_speed()
    elif key == arcade.key.S:
      self.player1.down_pressed = True
    self.player1.set_speed()
    
    # Player 2 controls
    if self.mode == 2 and key == arcade.key.UP:
      self.player2.up_pressed = True
      self.player2.set_speed()
    elif self.mode == 2 and key == arcade.key.DOWN:
      self.player2.down_pressed = True
      self.player2.set_speed()

    # start ball movement on spacebar press
    if not self.started and key == arcade.key.SPACE:
      self.started = True
      # Randomize initial ball direction
      movement_choice = random.randint(1, 4)
      match movement_choice:
        case 1:
          self.ball_sprite.move_up()
          self.ball_sprite.move_right()
        case 2:
          self.ball_sprite.move_up()
          self.ball_sprite.move_left()
        case 3:
          self.ball_sprite.move_down()
          self.ball_sprite.move_right()
        case 4:
          self.ball_sprite.move_down()
          self.ball_sprite.move_left()

    # Switch between 1 player and 2 player mode
    if self.started == False and key == arcade.key.TAB:
      if self.mode == 2:
        self.mode = 1
        self.mode_text.text = "1 Player Mode"
        self.switch_mode_text.text = "Press Tab to switch to 2 Player Mode"
      else:
        self.mode = 2
        self.mode_text.text = "2 Player Mode"
        self.switch_mode_text.text = "Press Tab to switch to 1 Player Mode"

  def on_key_release(self, key, modifiers):
    # Player 1 controls
    if key == arcade.key.W:
      self.player1.up_pressed = False
      self.player1.set_speed()
    if key == arcade.key.S:
      self.player1.down_pressed = False
      self.player1.set_speed()
    
    # Player 2 controls
    if self.mode == 2 and key == arcade.key.UP:
      self.player2.up_pressed = False
      self.player2.set_speed()
    if self.mode == 2 and key == arcade.key.DOWN:
      self.player2.down_pressed = False
      self.player2.set_speed()

  def set_bounce_angle(self, paddle: Paddle):
    """Function created by copilot AI. Used AI to write the math required to set
    the bounce angle based on where the ball hits the paddle. I do understand 
    what it is doing now, but I would not have been able to figure this out myself
    in the time I had available.
    """
    # Calculate the difference in y position between the ball and the paddle center
    y_diff = self.ball_sprite.center_y - paddle.center_y
    # Normalize the difference to a range of -1 to 1
    normalized_diff = y_diff / (paddle.height / 2)
    # Set the ball's vertical speed based on the normalized difference
    self.ball_sprite.change_y = normalized_diff * self.ball_sprite.y_movement

# Main code entry point
if __name__ == "__main__":
  app = Pong(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
  app.setup()
  arcade.run()