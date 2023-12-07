from globals import *
from map import Map
from creatures import *
import random


class World:
    __tick = TICK
    __time_elapsed = 0

    __map = None
    __creatures = []

    def __init__(self, map_size: tuple, predators: int, preys: int) -> None:
        self.__map = Map(map_size[0], map_size[1])

        for _ in range(predators):
            while True:
                position = (random.randint(0, map_size[0] - 1),
                            random.randint(0, map_size[1] - 1))
                if not any(c.position == position for c in self.__creatures):
                    self.__creatures.append(Predator(position))
                    break

        for _ in range(preys):
            while True:
                position = (random.randint(0, map_size[0] - 1),
                            random.randint(0, map_size[1] - 1))
                if not any(c.position == position for c in self.__creatures):
                    self.__creatures.append(Prey(position))
                    break

    """
    Goes to the next world state
    """
    def __next_step(self):
        self.__map.update()

        dead_list = [creature for creature in self.__creatures if not creature.is_alive()]
        for creature in dead_list:
            self.__creatures.remove(creature)

        for creature in self.__creatures:
            creature.update(self.__map, self.__creatures)

    """
    Updates the parts of the world
    """
    def update(self, delta_time):
        self.__time_elapsed += delta_time

        if self.__time_elapsed >= self.__tick:
            self.__next_step()
            self.__time_elapsed = 0

    """
    Draws the parts of the world
    """
    def draw(self, screen):
        self.__map.draw(screen)

        for creature in self.__creatures:
            creature.draw(screen)
