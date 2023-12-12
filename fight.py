import random
from random import shuffle
from creature_type import CreatureType
from datetime import datetime


class Fight:
    def __init__(self, *creatures) -> None:
        self.__start = datetime.now().time()
        self.__end = None

        self.__creatures = list(creatures)
        self.__survivors = []
        self.__is_conducted = False

        self.__creatures_string = "; ".join([str(creature) for creature in self.__creatures])
        self.__survivors_string = ""

        for creature in self.__creatures:
            creature.is_in_fight = True

    """
    Conducts a fight between some number of creatures
    """
    def conduct(self):
        if self.__is_conducted:
            return

        type_set = set(creature.creature_type for creature in self.__creatures)
        if len(type_set) == 1:
            for creature in self.__creatures:
                creature.is_in_fight = False
            return

        shuffle(self.__creatures)

        self.__survivors = self.__creatures
        if len(self.__survivors) == len(self.__creatures):
            for attacker in self.__creatures:
                if not attacker:
                    continue

                targets = [target for target in self.__creatures if
                           target != attacker and target.creature_type != attacker.creature_type]

                if not targets:
                    continue

                shuffle(targets)

                targets[0].take_damage(attacker.strength)

            self.__survivors = [creature for creature in self.__creatures if creature]

            type_set = set(survivor.creature_type for survivor in self.__survivors)

            if len(type_set) == 1:
                self.__survivors_string = "; ".join([str(creature) for creature in self.__survivors])

                for survivor in self.__survivors:
                    if survivor.creature_type == CreatureType.Predator:
                        survivor.restore()
                    survivor.is_in_fight = False

                self.__is_conducted = True
                self.__end = datetime.now().time()

    """
    Returns the state of fight conduction
    """
    def __bool__(self):
        return self.__is_conducted

    """
    Returns the string of the fight
    """
    def __str__(self):
        if not self:
            return

        string = (f"Start time: {self.__start} | End time: {self.__end}\n"
                  f"Participants: {self.__creatures_string}\n"
                  f"Survivors: {self.__survivors_string}"
                  f"\n")
        return string
