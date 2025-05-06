import numpy as np
from scipy import stats
import math

class SeriesAnalyzer:
    def __init__(self, x_values, n_terms, eps=1e-6):
        self.x_values = np.array(x_values)
        self.n_terms = n_terms
        self.eps = eps
        self.series_results = []

    def series_sum(self, x):
        s = 0
        for n in range(1, self.n_terms + 1):  # n from 1
            term = 1 / ((2 * n + 1) * x ** (2 * n + 1))
            s += term
            if abs(term) < self.eps:
                break
        return 2 * s

    def analytic(self, x):
        return math.log((x + 1) / (x - 1)) - 2 / x

    def calculate(self):
        for x in self.x_values:
            fx = self.series_sum(x)
            fx_analytic = self.analytic(x)
            eps_val = abs(fx - fx_analytic)
            self.series_results.append({
                'x': x,
                'n': self.n_terms,
                'F(x)': fx,
                'Math F(x)': fx_analytic,
                'eps': eps_val
            })

    def get_statistics(self, key):
        values = [res[key] for res in self.series_results]
        mean = np.mean(values)
        median = np.median(values)
        mode = stats.mode(values, keepdims=False).mode
        var = np.var(values)
        std = np.std(values)
        return {
            'mean': mean,
            'median': median,
            'mode': mode,
            'variance': var,
            'std': std
        } 