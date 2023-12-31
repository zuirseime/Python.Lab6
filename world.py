from globals import *
from map import Map
from creatures import Predator, Prey, Creature
from fight import Fight
import random
from pygame import Surface


class World:
    __tick = TICK

    def __init__(self, map_size: tuple, predators: int, preys: int) -> None:
        self.__map = Map(map_size[0], map_size[1])
        self.__creatures = []
        self.__fights = []
        self.conducted_fights = []

        self.__time_elapsed = 0

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

    def __check_encounters(self) -> None:
        for fight in self.__fights:
            fight.conduct()

            if fight:
                self.conducted_fights.append(fight)
                self.__fights.remove(fight)

        for current in self.__creatures:
            if not current or current.is_in_fight:
                continue

            targets = [target for target in self.__creatures if
                       target is not current and
                       current.creature_type != target.creature_type and
                       not target.is_in_fight and
                       self.__are_adjacent(current, target)]

            if not targets:
                return

            self.__fights.append(Fight(current, *targets))

    @staticmethod
    def __are_adjacent(attacker: Creature, current: Creature) -> bool:
        return (abs(attacker.position[0] - current.position[0]) <= 1 and
                abs(attacker.position[1] - current.position[1]) <= 1)

    """
    Goes to the next world state
    """
    def __next_step(self) -> None:
        self.__check_encounters()

        self.__map.update()

        for creature in self.__creatures:
            if not creature:
                self.__creatures.remove(creature)
            creature.update(self.__map, self.__creatures)

    """
    Updates the parts of the world
    """
    def update(self, delta_time: int) -> None:
        self.__time_elapsed += delta_time

        if self.__time_elapsed >= self.__tick:
            self.__next_step()
            self.__time_elapsed = 0

    """
    Draws the parts of the world
    """
    def draw(self, screen: Surface) -> None:
        self.__map.draw(screen)

        for creature in self.__creatures:
            creature.draw(screen)
