import arcade

class Paddle(arcade.Sprite):
  """Paddle class for the Pong game.
  Requires an image file for the sprite and a scaling factor."""

  def __init__(self, image_file: str, scale: float):

    # Initialize the parent class
    super().__init__(image_file, scale)

    # Initializing movement flags and speed
    self.up_pressed = False
    self.down_pressed = False
    self.movement_speed = 5
  
  def update(self, delta_time: float):

    # Call the parent update method
    super().update()

    # Keep the paddle within the screen bounds
    if self.top > arcade.get_window().height:
        self.top = arcade.get_window().height
    if self.bottom < 0:
        self.bottom = 0

  # Set paddle speed based on key presses
  # This is different than the default arcade way to 
  # allow for smoother movement
  def set_speed(self):
    if self.up_pressed and not self.down_pressed:
      self.change_y = self.movement_speed
    elif self.down_pressed and not self.up_pressed:
      self.change_y = -self.movement_speed
    else:
      self.change_y = 0
