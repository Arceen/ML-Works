class SnakeBody:
    x = 0
    y = 0
    next = None
    head = False
    def __init__(self, x, y, head):
        self.x = x
        self.y = y
        self.head = head
    #Set this if this is not the tail / remain None if tail
    def setNext(self, next):
        self.next = next