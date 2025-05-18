from abc import ABC, abstractmethod
import math

class Shape(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

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

class IsoscelesTriangle(Shape):
    def __init__(self, base, height, color):
        super().__init__(name="Равнобедренный треугольник")
        self.base = base
        self.height = height
        self._color_obj = FigureColor(color)
       # self.name = 'Равнобедренный треугольник'

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