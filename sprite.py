import pygame
from globals import *

textures = {}

texture_data = {
    'cell':             { 'type': 'cell',     'file_path': 'resources/cell.png',           'size': (SPRITE_SIZE, SPRITE_SIZE) },
    'grass':            { 'type': 'grass',    'file_path': 'resources/grass.png',          'size': (SPRITE_SIZE, SPRITE_SIZE) },
    'predator':         { 'type': 'creature', 'file_path': 'resources/predator.png',       'size': (SPRITE_SIZE, SPRITE_SIZE) },
    'prey':             { 'type': 'creature', 'file_path': 'resources/prey.png',           'size': (SPRITE_SIZE, SPRITE_SIZE) },
    'predator_steps':   { 'type': 'steps',    'file_path': 'resources/predator_steps.png', 'size': (SPRITE_SIZE, SPRITE_SIZE) },
    'prey_steps':       { 'type': 'steps',    'file_path': 'resources/prey_steps.png',     'size': (SPRITE_SIZE, SPRITE_SIZE) },
}

class Sprite:
    def __init__(self, name: str, position: tuple) -> None:
        self.image = self.get_texture(name)
        self.position = (position[0], position[1])

    def draw(self, surface):
        position = (self.position[0] * SPRITE_SIZE, self.position[1] * SPRITE_SIZE)
        surface.blit(self.image, position)

    @staticmethod
    def gen_textures() -> dict:
        for name, data in texture_data.items():
            textures[name] = pygame.transform.scale(pygame.image.load(data['file_path']).convert_alpha(), (data['size']))

    @staticmethod
    def get_texture(name: str):
        return textures[name]