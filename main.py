import pygame
from globals import *
from world import World
from sprite import Sprite


class Simulator:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("ЛР6 Кібець")

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        Sprite.gen_textures()

        self.running = True

        self.world = World(MAP_SIZE, PREDATOR_NUMBER, PREY_NUMBER)

    """
    Runs the pygame window
    """
    def run(self):
        while self.running:
            self.update()
            self.draw()

        self.close()

    """
    Updates the pygame window
    """
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill((173, 216, 230))

        self.world.update(self.clock.tick(FPS))

    """
    Draws the pygame window
    """
    def draw(self):
        self.world.draw(self.screen)

        pygame.display.flip()

    """
    Closes the pygame window
    """
    def close(self):
        pygame.quit()


if __name__ == "__main__":
    simulator = Simulator()
    simulator.run()
