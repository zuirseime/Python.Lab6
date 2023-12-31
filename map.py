from pygame import Surface
from cell import Cell


class Map:
    def __init__(self, width: int, height: int) -> None:
        self.data = [[Cell((x, y)) for y in range(height)] for x in range(width)]

    def width(self) -> int:
        return len(self.data)

    def height(self) -> int:
        return len(self.data[0])

    """
    Updates the map elements
    """
    def update(self) -> None:
        for row in self.data:
            for cell in row:
                cell.update()

    """
    Draws the map elements
    """
    def draw(self, surface: Surface) -> None:
        for row in self.data:
            for cell in row:
                cell.draw(surface)

    """
    Checks if a certain position is within the map
    """
    def contains(self, position: tuple) -> bool:
        return self.__contains(position[0], position[1])

    """
    Checks if a certain position is within the map
    """
    def __contains(self, x: int, y: int) -> bool:
        return 0 <= x < self.width() and 0 <= y < self.height()
