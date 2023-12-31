from cell import Cell
from sprite import Sprite
from creature_type import CreatureType
from map import Map
import random


class Creature(Sprite):
    __count = 0

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    map = None
    creatures = None

    def __init__(self, name: str, position: tuple,
                 creature_type: CreatureType,
                 max_hp: int = 10, max_strength: int = 10, max_hunger: int = 10) -> None:
        super().__init__(name, position)
        self.id = Creature.__count
        Creature.__count += 1

        self.creature_type = creature_type
        self.base_hp = max_hp
        self.heal_points = max_hp
        self.base_strength = max_strength
        self.strength = max_strength
        self.max_hunger = max_hunger
        self.hunger = 0

        self.is_in_fight = False
        self.direction = (0, 0)

    """
    Takes a damage from another creature
    """
    def take_damage(self, damage: int) -> None:
        if self.__is_alive():
            self.heal_points -= damage

    """
    Makes the creature die
    """
    def die(self) -> None:
        self.heal_points = 0

    """
    Checks if the creature is alive
    """
    def __is_alive(self) -> bool:
        return self.heal_points > 0

    """
    Restores creature parameters
    """
    def restore(self, target) -> None:
        self.hunger = 0
        self.heal_points = self.base_hp
        self.strength = self.base_strength

    """
    Updates creature state
    """
    def update(self, map: Map, creatures: list) -> None:
        self.map = map
        self.creatures = creatures

        if not self.is_in_fight:
            if self.hunger < self.max_hunger:
                self.hunger += 1
            elif self.strength > 0:
                self.strength -= 1

            if self.strength <= self.base_strength / 2:
                self.heal_points -= 1

        if not self.__is_alive():
            self.die()

    """
    Moves the creature to another position
    """
    def _move(self, destination: tuple) -> None:
        self.map.data[self.position[0]][self.position[1]].walk_through(self.creature_type)
        self.position = destination

    """
    Confirms move
    """
    def __confirm_move(self, destination, condition) -> bool:
        if condition:
            self.direction = (destination[0] - self.position[0], destination[1] - self.position[1])
            self._move(destination)
            return True
        return False

    """
    Tries to choose random way to move
    """
    def _choose_random_way(self) -> bool:
        while True:
            raw_direction = random.choice(self.directions)

            destination = (self.position[0] + raw_direction[0], self.position[1] + raw_direction[1])

            if self.map.contains(destination):
                condition = not any(c.position == destination for c in self.creatures)
                return self.__confirm_move(destination, condition)

    """
    Tries to look for food around
    """
    def _look_for_food(self) -> bool:
        destination = self.position

        for direction in self.directions:
            new_position = (self.position[0] + direction[0], self.position[1] + direction[1])

            if self.map.contains(new_position):
                x = new_position[0]
                y = new_position[1]
                if (isinstance(self, Prey) and self.map.data[x][y].has_grass or
                        isinstance(self, Predator) and any(isinstance(c, Prey)
                                                           and c.position == new_position for c in self.creatures)):
                    destination = new_position

        return self.__confirm_move(destination, destination != self.position)

    """
    Tries to look for traces around
    """
    def _look_for_traces(self, limit: float, func) -> bool:
        destination = self.position

        for direction in self.directions:
            new_position = (self.position[0] + direction[0], self.position[1] + direction[1])

            if self.map.contains(new_position):
                value = self.map.data[new_position[0]][new_position[1]].trace_magnitude
                trace = self.map.data[new_position[0]][new_position[1]].trace_status

                is_destination_free = not any(c.position == new_position for c in self.creatures)
                is_the_enemy_trace = trace != 0 and trace != self.creature_type
                is_weight_match = func(value, limit)

                if value != 0 and is_destination_free and is_the_enemy_trace and is_weight_match:
                    limit = value
                    destination = new_position

        return self.__confirm_move(destination, destination != self.position)

    """
    Builds the string of creature parameters
    """
    def __str__(self) -> str:
        return (f"{self.creature_type.name}{self.id} | "
                f"HP: {self.heal_points}/{self.base_hp} "
                f"S: {self.strength}/{self.base_strength} "
                f"H: {self.hunger}/{self.max_hunger}")

    """
    Checks if the creature is alive
    """
    def __bool__(self) -> bool:
        return self.__is_alive()


class Prey(Creature):
    def __init__(self, position: tuple) -> None:
        super().__init__("prey", position, CreatureType.Prey, 100, 5, 10)

    """
    Moves the creature to another position
    """
    def _move(self, destination: tuple) -> None:
        super()._move(destination)

        if self.map.contains(self.position):
            cell = self.map.data[self.position[0]][self.position[1]]

            if cell.has_grass and not self.is_in_fight:
                self.restore(cell)

    """
    Restores creature parameters
    """
    def restore(self, cell: Cell) -> None:
        super().restore(cell)
        cell.has_grass = False

    """
    Updates creature state
    """
    def update(self, map: Map, creatures: list[Creature]) -> None:
        super().update(map, creatures)

        if not self.is_in_fight:
            if self.hunger == self.max_hunger:
                if self._look_for_food():
                    return

            if self._look_for_traces(float('inf'), lambda v, l: v < l):
                return
            self._choose_random_way()


class Predator(Creature):
    def __init__(self, position: tuple) -> None:
        super().__init__("predator", position, CreatureType.Predator, 200, 20, 15)

    """
    Restores creature parameters
    """
    def restore(self, target: Creature = None) -> None:
        super().restore(target)

    """
    Updates creature state
    """
    def update(self, map: Map, creatures: list[Creature]) -> None:
        super().update(map, creatures)

        if not self.is_in_fight:
            if self._look_for_food():
                return
            if self._look_for_traces(float('-inf'), lambda v, l: v > l):
                return
            self._choose_random_way()
