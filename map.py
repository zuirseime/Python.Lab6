from globals import *
from cell import Cell

class Map:
    def __init__(self, width, height) -> None:
        self.__width = width
        self.__height = height

        self.data = [[Cell((x, y)) for y in range(height)] for x in range(width)]

    def update(self):
        for row in self.data:
            for cell in row:
                cell.update()

    def draw(self, surface):
        for row in self.data:
            for cell in row:
                cell.draw(surface)

    def contains(self, position: tuple):
        return self.__contains(position[0], position[1])
    
    def __contains(self, x: int, y: int):
        return x >= 0 and x < self.__width and y >= 0 and y < self.__height