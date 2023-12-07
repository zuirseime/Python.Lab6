from cell import Cell


class Map:
    def __init__(self, width, height) -> None:
        self.__width = width
        self.__height = height

        self.data = [[Cell((x, y)) for y in range(height)] for x in range(width)]

    """
    Updates the map elements
    """
    def update(self):
        for row in self.data:
            for cell in row:
                cell.update()

    """
    Draws the map elements
    """
    def draw(self, surface):
        for row in self.data:
            for cell in row:
                cell.draw(surface)

    """
    Checks if a certain position is within the map
    """
    def contains(self, position: tuple):
        return self.__contains(position[0], position[1])

    """
    Checks if a certain position is within the map
    """
    def __contains(self, x: int, y: int):
        return 0 <= x < self.__width and 0 <= y < self.__height
