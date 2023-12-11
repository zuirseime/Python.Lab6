from sprite import Sprite
from fight import Fight
from creature_type import CreatureType
import random


class Creature(Sprite):
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    map = None
    creatures = None

    def __init__(self, name: str, position: tuple,
                 creature_type: CreatureType,
                 max_hp: int = 10, max_strength: int = 10, max_hunger: int = 10) -> None:
        super().__init__(name, position)
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
    Conducts a fight
    """
    @staticmethod
    def conduct_fight(random_order: bool, *creatures):
        for creature in creatures:
            creature.is_in_fight = True

        if len(creatures) > 0:
            fight = Fight(*creatures)
            fight.conduct(random_order)

            if fight:
                print(fight)

    """
    Takes a damage from another creature
    """
    def take_damage(self, damage: int):
        if self.__is_alive():
            self.heal_points -= damage

    """
    Makes the creature die
    """
    def die(self):
        self.heal_points = 0

    """
    Checks if the creature is alive
    """
    def __is_alive(self):
        return self.heal_points > 0

    """
    Restores creature parameters
    """
    def restore(self, target):
        self.hunger = 0
        self.heal_points = self.base_hp
        self.strength = self.base_strength

    """
    Updates creature state
    """
    def update(self, map, creatures: list):
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
    def _move(self, destination: tuple):
        self.map.data[self.position[0]][self.position[1]].walk_through(self.creature_type)
        self.position = destination

    """
    Confirms move
    """
    def __confirm_move(self, destination, condition):
        if condition:
            self.direction = (destination[0] - self.position[0], destination[1] - self.position[1])
            self._move(destination)
            return True
        return False

    """
    Makes the creature look for the enemy around
    """
    def _look_for_enemy(self):
        adjacent_creatures = [creature for creature in self.creatures if creature is not self]

        self.__attack_if_adjacent(*adjacent_creatures)

    """
    Checks if a certain creature is adjacent to this one
    """
    def __is_adjacent(self, other):
        return abs(self.position[0] - other.position[0]) <= 1 and abs(self.position[1] - other.position[1]) <= 1

    """
    Makes creature attack certain creatures if they are adjacent to this one
    """
    def __attack_if_adjacent(self, *creatures):
        fighters = [fighter for fighter in creatures if self.__is_adjacent(fighter)
                    and isinstance(fighter, Creature)
                    and self.creature_type != fighter.creature_type
                    and not fighter.is_in_fight]

        if fighters:
            self.conduct_fight(True, *fighters)

    """
    Tries to choose random way to move
    """
    def _choose_random_way(self):
        while True:
            raw_direction = random.choice(self.directions)

            destination = (self.position[0] + raw_direction[0], self.position[1] + raw_direction[1])

            if self.map.contains(destination):
                condition = not any(c.position == destination for c in self.creatures)
                return self.__confirm_move(destination, condition)

    """
    Tries to look for food around
    """
    def _look_for_food(self):
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
    def _look_for_traces(self, limit: float, func):
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
    def __str__(self):
        return (f"{self.position} {self.creature_type} | "
                f"HP: {self.heal_points}/{self.base_hp} "
                f"S: {self.strength}/{self.base_strength} "
                f"H: {self.hunger}/{self.max_hunger}")

    """
    Checks if the creature is alive
    """
    def __bool__(self):
        return self.__is_alive()


class Prey(Creature):
    def __init__(self, position: tuple) -> None:
        super().__init__("prey", position, CreatureType.Prey, 100, 5, 10)

    """
    Moves the creature to another position
    """
    def _move(self, destination: tuple):
        super()._move(destination)

        if self.map.contains(self.position):
            cell = self.map.data[self.position[0]][self.position[1]]

            if cell.has_grass and not self.is_in_fight:
                self.restore(cell)

    """
    Restores creature parameters
    """
    def restore(self, cell):
        super().restore(cell)
        cell.has_grass = False

    """
    Updates creature state
    """
    def update(self, map, creatures):
        super().update(map, creatures)

        if self.hunger == self.max_hunger:
            if self._look_for_food():
                return

        if self._look_for_traces(float('inf'), lambda v, l: v < l):
            return
        self._choose_random_way()

        self._look_for_enemy()


class Predator(Creature):
    def __init__(self, position: tuple) -> None:
        super().__init__("predator", position, CreatureType.Predator, 200, 20, 15)

    """
    Moves the creature to another position
    """
    def _move(self, destination):
        super()._move(destination)

        target = next((creature for creature in self.creatures if isinstance(creature, Prey)
                       and creature.position == destination), None)
        if target and not self.is_in_fight:
            self.conduct_fight(False, self, target)

    """
    Restores creature parameters
    """
    def restore(self, target=None):
        super().restore(target)

    """
    Updates creature state
    """
    def update(self, map, creatures):
        super().update(map, creatures)

        if self._look_for_food():
            return
        if self._look_for_traces(float('-inf'), lambda v, l: v > l):
            return
        self._choose_random_way()

        self._look_for_enemy()
