
class Snake:

    def __init__(self):
        self.head = Body((0, 0), None)
        self.tail = Body(None, self.head)
        self.snake = {self.head.coordinate: self.head}
        self.snake_color = (79, 132, 55)

class Body:
    def __init__(self, coordinate, next):
        self.coordinate = coordinate
        self.next = next

    def __eq__(self, other):
        return self.coordinate == other.coordinate
