import matplotlib.pyplot as plt
from shapes import IsoscelesTriangle

def validate_positive_float(value, name):
    try:
        val = float(value)
        if val <= 0:
            raise ValueError
        return val
    except ValueError:
        raise ValueError(f"{name} должно быть положительным числом!")

def draw_triangle(triangle: IsoscelesTriangle, label: str, filename=None):
    a = triangle.base
    h = triangle.height
    # Вершины: A (0,0), B (a,0), C (a/2, h)
    x = [0, a, a/2, 0]
    y = [0, 0, h, 0]
    plt.figure(figsize=(6,6))
    plt.fill(x, y, color=triangle.color, alpha=0.5)
    plt.plot(x, y, color='black')
    plt.text(a/2, h/2, label, ha='center', va='center', fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    plt.title(triangle.name)
    plt.axis('equal')
    plt.axis('off')
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    plt.show() 