import arcade

class Ball(arcade.Sprite):
  
  def __init__(self, image_file: str, scale: float, DIR_PATH: str):

    # Initialize the parent class
    super().__init__(image_file, scale)

    # Set initial movement speed
    self.y_movement = 3

    # Load sound for hitting top and bottom
    self.hit_top_bottom_sound = arcade.load_sound(f"{DIR_PATH}/sounds/hit_top_bottom.wav")
  
  def update(self, delta_time: float):

    # Call the parent update method
    super().update()

    # Bounce off top and bottom of screen
    if self.top > arcade.get_window().height:
      arcade.play_sound(self.hit_top_bottom_sound)
      self.top = arcade.get_window().height
      self.move_down()
    if self.bottom < 0:
      arcade.play_sound(self.hit_top_bottom_sound)
      self.bottom = 0
      self.move_up()

  # Movement methods
  # This is more similar to the default arcade method
  # of creating movement for sprites
  # I've wrapped them in methods for clarity
  # in the main game file.
  def move_up(self):
    self.change_y = self.y_movement

  def move_down(self):
    self.change_y = -self.y_movement

  def move_right(self):
    self.change_x = 5

  def move_left(self):
    self.change_x = -5

  # Stop all movement
  # Used when a player scores
  def stop_moving(self):
    self.change_y = 0
    self.change_x = 0
