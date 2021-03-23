class Drone:
    def __init__(self, x, y):
        self._x, self._y = x, y

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, value):
        self._x, self._y = value
