class CreatureConfiguration:
  def __init__(self, count, attract=True, space=10, speed=3 ) :
    self.count = count
    self.attract = attract
    self.speed = speed
    self.space = space

class LightConfiguration:
  def __init__(self, count, speed=5, random=True):
    self.count = count
    self.speed = speed
    self.random = random

example = [0,0]
example[0] = ( CreatureConfiguration( 10, True, 100, 8),
             LightConfiguration( 2, 3 ) )

example[1] = ( CreatureConfiguration( 5, True, 10, 5 ),
             CreatureConfiguration( 10, False, 10, 5),
             LightConfiguration( 5, 5 ))
