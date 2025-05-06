import numpy as np

def generate_matrix(n, m, low=0, high=10):
    return np.random.randint(low, high, size=(n, m))

def find_min_sum_column(matrix):
    col_sums = matrix.sum(axis=0)
    min_col_idx = np.argmin(col_sums)
    return min_col_idx, matrix[:, min_col_idx], col_sums[min_col_idx]

def manual_median(arr):
    arr_sorted = np.sort(arr)
    n = len(arr_sorted)
    if n % 2 == 1:
        return arr_sorted[n // 2]
    else:
        return (arr_sorted[n // 2 - 1] + arr_sorted[n // 2]) / 2 