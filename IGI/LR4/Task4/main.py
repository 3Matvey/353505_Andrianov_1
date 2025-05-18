from shapes import IsoscelesTriangle
from utils import validate_positive_float, draw_triangle

def main():
    print('Построение равнобедренного треугольника')
    while True:
        try:
            base = validate_positive_float(input('Введите основание a: '), 'Основание')
            height = validate_positive_float(input('Введите высоту h: '), 'Высота')
            color = input('Введите цвет (например, blue, red, green): ').strip()
            label = input('Введите подпись для фигуры: ').strip()
            break
        except ValueError as e:
            print(e)
    triangle = IsoscelesTriangle(base, height, color)
    print(triangle)
    draw_triangle(triangle, label, filename='triangle.png')
    with open('triangle.txt', 'w', encoding='utf-8') as f:
        f.write(str(triangle) + '\n')
        f.write(f'Подпись: {label}\n')

if __name__ == '__main__':
    main()