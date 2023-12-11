import pygame
from pygame import Surface
from globals import *


class Sprite:
    textures = {}

    raw_textures_data = {
        'cell': {'type': 'cell', 'file_path': 'res/cell.png', 'size': (SPRITE_SIZE, SPRITE_SIZE)},
        'grass': {'type': 'grass', 'file_path': 'res/grass.png', 'size': (SPRITE_SIZE, SPRITE_SIZE)},
        'predator': {'type': 'creature', 'file_path': 'res/predator.png', 'size': (SPRITE_SIZE, SPRITE_SIZE)},
        'prey': {'type': 'creature', 'file_path': 'res/prey.png', 'size': (SPRITE_SIZE, SPRITE_SIZE)},
        'predator_steps': {'type': 'steps', 'file_path': 'res/predator_steps.png', 'size': (SPRITE_SIZE, SPRITE_SIZE)},
        'prey_steps': {'type': 'steps', 'file_path': 'res/prey_steps.png', 'size': (SPRITE_SIZE, SPRITE_SIZE)},
    }

    def __init__(self, name: str, position: tuple) -> None:
        self.image = self.get_texture(name)
        self.position = (position[0], position[1])

    """
    Draws the sprite
    """
    def draw(self, surface: Surface):
        position = (self.position[0] * SPRITE_SIZE, self.position[1] * SPRITE_SIZE)
        surface.blit(self.image, position)

    """
    Generates sprite textures from pictures
    """
    @staticmethod
    def gen_textures() -> None:
        for name, data in Sprite.raw_textures_data.items():
            Sprite.textures[name] = pygame.transform.scale(pygame.image.load(data['file_path']).convert_alpha(), (data['size']))

    """
    Gives a certain sprite texture
    """
    @staticmethod
    def get_texture(name: str) -> Surface:
        return Sprite.textures[name]
