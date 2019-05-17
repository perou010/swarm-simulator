import turtle
import math
from random import uniform
from random import randint
import entities
import config

# When testing the spacing, make sure to use at least a value of 50 to really see the effect
# Will work with any combination of creatures and lights from the configuartion (even zero of either or each)

class Arena:
    def __init__(self, test_configuration):
        self.creatures = []
        self.lights = []
        # addition is an isinstance of the CreatureConfiguration or LightConfiguration class
        # adds new instnaces of the entity based on the given configuration class
        for addition in test_configuration:
            if isinstance(addition, config.CreatureConfiguration):
                for i in range(addition.count):
                    self.creatures.append(entities.Creature(addition.speed, addition.space, addition.attract))
            elif isinstance(addition, config.LightConfiguration):
                for i in range(addition.count):
                    self.lights.append(entities.Light(addition.speed, addition.random))

    def init_graphics(self):
        turtle.setworldcoordinates(-25,-25,1025,1025)
        self.backgroundTurtle = turtle.Turtle()
        self.backgroundTurtle.pu()
        self.backgroundTurtle.ht()
        self.backgroundTurtle.goto(-50,-50)
        self.backgroundTurtle.color('grey')
        self.backgroundTurtle.begin_fill()
        for i in range(4):
            self.backgroundTurtle.forward(1100)
            self.backgroundTurtle.left(90)
        self.backgroundTurtle.end_fill()
        self.backgroundTurtle.goto(0,0)
        self.backgroundTurtle.color('lightblue')
        self.backgroundTurtle.begin_fill()
        for i in range(4):
            self.backgroundTurtle.forward(1000)
            self.backgroundTurtle.left(90)
        self.backgroundTurtle.end_fill()
        turtle.update()

    def move(self, entity):
        # Randomizes the heading 1 out of every 40 updates on average if the light.random is set to True
        if isinstance(entity, entities.Light):
            if entity.random:
                if randint(0,1000) >= 975:
                    entity.set_heading(uniform(-math.pi, math.pi))

        # Updates a creature's heading based on its spacing factor and how close it is the the light
        if isinstance(entity, entities.Creature):
            # for each creature within the self's space, a vector pointing in the opposite direction will be added to this list
            away_vectors = []
            net_away_vector = entity.velocity
            for nearby_creature in self.creatures:
                # making sure to not factor itself into the calulation
                if (nearby_creature.heading != entity.heading) and (nearby_creature.position != entity.position):
                    if entity.find_distance(nearby_creature) <= entity.space:
                        away_vectors.append(entities.Vector(entity.position[0] - nearby_creature.position[0], entity.position[1] - nearby_creature.position[1]))
            for away_vector in away_vectors:
                # add up all of the away vecotrs, scale it, and apply it to the self's main velocity vector
                net_away_vector += away_vector.scale(.05)

            entity.set_heading(net_away_vector.get_heading())

            # shift towards (or away) from the light:
            if len(self.lights) != 0:
                for light in self.lights:
                    distance_to_light = entity.find_distance(light)
                    # the degree to which the distance from the light influences the heading of the creature is a scaled upside down parabola.
                    # a light passed 800 distance away does not influnce the creature at all
                    if distance_to_light < 800:
                        degree_of_attraction = -((1 / 800) * distance_to_light) ** 2 + 1
                    else:
                        degree_of_attraction = 0
                    # here if the creatures are attracted to the light
                    if entity.attract:
                        towards_light_vector = entities.Vector(-entity.position[0] + light.position[0], -entity.position[1] + light.position[1])
                    # here if the creature are repulsed by lights
                    elif not entity.attract:
                        towards_light_vector = entities.Vector(-(-entity.position[0] + light.position[0]), -(-entity.position[1] + light.position[1]))
                    # net vector scaled by a number(depedendent on its degree of attraction and a number to determine how strong light attraction is overall)
                    entity.velocity += entities.Vector(entity.speed * math.cos(towards_light_vector.get_heading()), entity.speed * math.sin(towards_light_vector.get_heading())).scale(degree_of_attraction / 10)


        # Collision between two moving creatures
        # based on the flatRedBall collision stuff, but not exactly
        # if isinstance(entity, entities.Creature):
        for nearby_entity in self.creatures + self.lights:
            # making sure it isn't able to collide with itself
            if (nearby_entity.heading != entity.heading) and (nearby_entity.position != entity.position):
                if entity.find_distance(nearby_entity) <= 2 * entity.radius:
                    new_vector = entities.Vector(entity.position[0] - nearby_entity.position[0], entity.position[1] - nearby_entity.position[1])
                    new_heading = new_vector.heading
                    # next 4 lines are for updating the nearby_entity's heading
                    if new_heading > 0:
                        nearby_entity.set_heading(new_heading - math.pi)
                    elif new_heading <= 0:
                        nearby_entity.set_heading(new_heading + math.pi)
                    # updating the other creature's (entity) heading
                    entity.set_heading(new_heading)

        # for collisions with wall for entities (lights and creatures)
        # a potential_position based on all of the other factors
        # check the position, if it is outside of the bounds, it will set the heading to reflect off the wall (a Wall type object)
        potential_position = (entity.position[0] + entity.speed * math.cos(entity.heading), entity.position[1] + entity.speed * math.sin(entity.heading))
        if potential_position[0] < 0 + entity.radius:
            entity.set_heading(entities.determine_new_heading_stationary(entity, entities.Wall((0, entity.position[1]))))
        if potential_position[0] > 1000 - entity.radius:
            entity.set_heading(entities.determine_new_heading_stationary(entity, entities.Wall((1000, entity.position[1]))))
        if potential_position[1] < 0 + entity.radius:
            entity.set_heading(entities.determine_new_heading_stationary(entity, entities.Wall((entity.position[0], 0))))
        if potential_position[1] > 1000 - entity.radius:
            entity.set_heading(entities.determine_new_heading_stationary(entity, entities.Wall((entity.position[0], 1000))))
        entity.position = (entity.position[0] + entity.speed * math.cos(entity.heading), entity.position[1] + entity.speed * math.sin(entity.heading))

    def update(self):
        """moves and draws creatures and lights"""
        for entity_list in [self.creatures, self.lights]:
            for entity in entity_list:
                self.move(entity)
                entity.draw_entity()

def main():
    turtle.tracer(0,0)
    arena = Arena(config.example[0])
    arena.init_graphics()
    try:
        while True:
            arena.update()
    except KeyboardInterrupt:
        print("Done swarming.")

if __name__ == '__main__':
    main()
