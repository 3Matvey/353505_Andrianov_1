from abc import ABC, abstractmethod
import math

class GeometricFigure(ABC):
    @abstractmethod
    def area(self):
        pass

class FigureColor:
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

class IsoscelesTriangle(GeometricFigure):
    def __init__(self, base, height, color):
        self.base = base
        self.height = height
        self._color_obj = FigureColor(color)
        self.name = 'Равнобедренный треугольник'

    @property
    def color(self):
        return self._color_obj.color

    @color.setter
    def color(self, value):
        self._color_obj.color = value

    def area(self):
        return 0.5 * self.base * self.height

    def __str__(self):
        return (f'{self.name}: основание={self.base}, высота={self.height}, '
                f'цвет={self.color}, площадь={self.area():.2f}') 