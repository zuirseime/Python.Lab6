from random import shuffle
from creature_type import CreatureType


class Fight:
    def __init__(self, *creatures) -> None:
        self.creatures = list(creatures)
        self.survivors = []
        self.is_conducted = False

    """
    Conducts a fight between some number of creatures
    """
    def conduct(self, random: bool):
        if self.is_conducted:
            return

        type_set = set(creature.creature_type for creature in self.creatures)
        if len(type_set) == 1:
            for creature in self.creatures:
                creature.is_in_fight = False
            return

        if random:
            shuffle(self.creatures)

        self.survivors = self.creatures
        while len(self.survivors) == len(self.creatures):
            for attacker in self.creatures:
                if not attacker.is_alive():
                    continue

                targets = [target for target in self.creatures if
                           target != attacker and target.creature_type != attacker.creature_type]

                if not targets:
                    continue

                for target in targets:
                    target.take_damage(attacker.strength)

            self.survivors = [creature for creature in self.creatures if creature.is_alive()]

            for survivor in self.survivors:
                if len(self.survivors) < len(self.creatures):
                    if survivor.creature_type == CreatureType.Predator:
                        survivor.restore()
                    survivor.is_in_fight = False

            self.is_conducted = True

    """
    Returns the state of fight conduction
    """
    def __bool__(self):
        return self.is_conducted

    """
    Returns the string of the fight
    """
    def __str__(self):
        return f"Fight conducted: {self.is_conducted}\nSurvivors:{[str(creature) for creature in self.survivors]}"
