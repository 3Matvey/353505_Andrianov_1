from .utils import generate_matrix, find_min_sum_column, manual_median
import numpy as np

def main():
    n = int(input('Введите количество строк (n): '))
    m = int(input('Введите количество столбцов (m): '))
    matrix = generate_matrix(n, m, low=0, high=20)
    print('Сгенерированная матрица:')
    print(matrix)
    idx, col, col_sum = find_min_sum_column(matrix)
    print(f'Столбец с минимальной суммой (индекс {idx}): {col}')
    print(f'Сумма элементов этого столбца: {col_sum}')
    median_np = np.median(col)
    median_manual = manual_median(col)
    print(f'Медиана этого столбца (numpy): {median_np}')
    print(f'Медиана этого столбца (ручной способ): {median_manual}')

if __name__ == '__main__':
    main()
