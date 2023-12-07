from sprite import Sprite
from creatures import CreatureType
import random

class Cell(Sprite):
    __grass_birth_probability = 0.2

    __grass_cooldown_state = 0
    __grass_cooldown = 5

    def __init__(self, position: tuple) -> None:
        super().__init__("cell", position)
        self.__grass_texture = Sprite("grass", position)
        self.__steps_texture = None
        self.has_grass = False
        self.trace_status = CreatureType.Null
        self.trace_magnitute = 0

    def walk_through(self, trace: CreatureType):
        self.trace_magnitute = 10
        self.trace_status = trace

        if trace == CreatureType.Predator:
            self.__steps_texture = Sprite("predator_steps", self.position)
        elif trace == CreatureType.Prey:
            self.__steps_texture = Sprite("prey_steps", self.position)

    def fade_out(self):
        self.trace_magnitute -= 1

    def grow_grass(self):
        if self.__grass_cooldown_state == self.__grass_cooldown:
            if random.random() <= self.__grass_birth_probability:
                self.has_grass = True
            else:
                self.__grass_cooldown_state = 0

    def update(self):
        if self.__grass_cooldown_state < self.__grass_cooldown:
            self.__grass_cooldown_state += 1
        else:
            self.grow_grass()

        if self.trace_magnitute > 0:
            self.fade_out()
        else:
            self.trace_status = CreatureType.Null
            self.__steps_texture = None

    def draw(self, surface):
        super().draw(surface)
        
        if self.has_grass is True:
            self.__grass_texture.draw(surface)

        if self.trace_magnitute != 0:
            self.__steps_texture.draw(surface)