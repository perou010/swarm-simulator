import turtle
import math
from random import uniform
from random import randint

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heading = math.atan2(y,x)

    def __add__(self, *vectors):
        net_vector = self
        for vector in vectors:
            self.x += vector.x
            self.y += vector.y
        return net_vector

    def scale(self, scalar):
        """Scales a vector by the given argument"""
        self.x = self.x * scalar
        self.y = self.y * scalar
        return Vector(self.x, self.y)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y **2)

    def get_heading(self):
        return math.atan2(self.y,self.x)

class Entity:
    def __init__(self, speed):
        self.entity_turtle = turtle.Turtle()
        self.heading = uniform(-math.pi, math.pi)
        self.speed = speed
        self.velocity = Vector(self.speed * math.cos(self.heading), self.speed * math.sin(self.heading))
        # Randomly assigned position whenever an entity is created
        self.position = (randint(15,985), randint(15,985))

    def draw_entity(self):
        # general drawing setup that does some setup then calls the specific entity's specific draw method
        self.entity_turtle.clear()
        self.entity_turtle.ht()
        self.entity_turtle.pu()
        self.draw()
        turtle.update()

    def find_distance(self, entity):
        return math.sqrt(((self.position[0] - entity.position[0]) ** 2) + ((self.position[1] - entity.position[1]) ** 2))

    def set_heading(self, heading):
        # setting the heading also updates the entity's velocity vector
        self.heading = heading
        self.velocity = Vector(self.speed * math.cos(self.heading), self.speed * math.sin(self.heading))

class Creature(Entity):
    def __init__(self, speed, space, attract):
        Entity.__init__(self, speed)
        self.radius = 15
        self.space = space
        self.attract = attract

    def draw(self):
        self.entity_turtle.goto(self.position[0], self.position[1] - self.radius)
        self.entity_turtle.color('pink')
        self.entity_turtle.pd()
        self.entity_turtle.begin_fill()
        self.entity_turtle.circle(self.radius)
        self.entity_turtle.end_fill()
        self.entity_turtle.pu()
        self.entity_turtle.goto(self.position[0] + self.radius * math.cos(self.heading), self.position[1] + self.radius * math.sin(self.heading) - self.radius / 5)
        self.entity_turtle.pd()
        self.entity_turtle.color('black')
        self.entity_turtle.begin_fill()
        self.entity_turtle.circle(self.radius / 5)
        self.entity_turtle.end_fill()

class Light(Entity):
    def __init__(self, speed, random):
        Entity.__init__(self, speed)
        self.random = random
        self.radius = 10

    def draw(self):
        self.entity_turtle.ht()
        self.entity_turtle.pu()
        for i in range(2):
            self.entity_turtle.goto(self.position[0], self.position[1] - [10, 7][i])
            self.entity_turtle.pd()
            self.entity_turtle.color(['yellow', 'white'][i])
            self.entity_turtle.begin_fill()
            self.entity_turtle.circle([10,7][i])
            self.entity_turtle.end_fill()

class Wall:
    """ Wall is just used in the collision triggered when an entity goes outside of the bounds"""
    def __init__(self, position):
        self.position = position

def determine_new_heading_stationary(creature, stationary):
    # determine pt of collision, which also defines the angle
    collision = Vector( stationary.position[0] - creature.position[0], \
                        stationary.position[1] - creature.position[1] )

    # define tangent to the point of collision
    collision_tangent = Vector( stationary.position[1] - creature.position[1], \
                                -(stationary.position[0] - creature.position[0]))

    # normalize the tangent making it length 1
    tangent_length = (collision_tangent.x ** 2 + collision_tangent.y ** 2) ** .5
    normal_tangent = Vector( collision_tangent.x / tangent_length, \
                             collision_tangent.y / tangent_length)

    # relative velocity = robot because stationary circle has 0 velocity
    rel_velocity = creature.velocity

    # determine the velocity vector along the tangent
    length = rel_velocity.x * normal_tangent.x + rel_velocity.y * normal_tangent.y
    tangent_velocity = Vector(normal_tangent.x * length, normal_tangent.y * length)

    # determine the velocity vector perpendicular to the tangent
    perpendicular = Vector(rel_velocity.x - tangent_velocity.x, \
                    rel_velocity.y - tangent_velocity.y )

    # new heading
    new_heading = Vector( (creature.velocity.x - 2 * perpendicular.x), \
                          (creature.velocity.y - 2 * perpendicular.y)  )

    return new_heading.heading
