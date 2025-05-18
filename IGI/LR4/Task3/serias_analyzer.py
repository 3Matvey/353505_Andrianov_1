import numpy as np
from scipy import stats
import math

class SeriesAnalyzer:
    """
    Анализатор ряда
        F(x) = 2 * sum_{n=0..∞} [1 / ((2n+1) * x^{2n+1})]
    и сравнение с аналитической функцией ln((x+1)/(x-1)).
    Собирает результаты по разным x и умеет считать статистику по любому полю.
    """
    def __init__(self, x_values, eps=1e-6):
        """
        x_values: iterable числовых значений x
        eps: порог для обрыва ряда
        """
        self.x_values = np.array(x_values, dtype=float)
        self.eps = eps
        self.series_results = []

    def series_sum(self, x: float) -> tuple[float,int]:
        """
        Вычисляет частичную сумму ряда F(x) до тех пор, 
        пока очередной член >= eps. 
        Возвращает (sum, фактическое число членов).
        """
        s = 0.0
        n = 0
        while True:
            term = 1.0 / ((2*n + 1) * x**(2*n + 1))
            if abs(term) < self.eps:
                break
            s += term
            n += 1
        # прибавляем n+1 членов (от 0 до n включительно) и домножаем на 2
        return 2 * s, n + 1

    def analytic(self, x: float) -> float:
        """
        Аналитическая функция, с которой сравниваем ряд.
        """
        return math.log((x + 1) / (x - 1))

    def calculate(self) -> None:
        """
        Заполняет self.series_results списком словарей:
        {'x': ..., 'n': ..., 'F(x)': ..., 'Math F(x)': ..., 'eps': ...}
        """
        self.series_results.clear()
        for x in self.x_values:
            fx, used_terms = self.series_sum(x)
            fx_analytic = self.analytic(x)
            diff = abs(fx - fx_analytic)
            self.series_results.append({
                'x': x,
                'n': used_terms,
                'F(x)': fx,
                'Math F(x)': fx_analytic,
                'eps': diff
            })

    def get_statistics(self, key: str) -> dict:
        """
        Для поля key из каждого результата строит:
        mean, median, mode, variance, std.
        """
        values = [res[key] for res in self.series_results]
        if not values:
            raise ValueError("Нет данных для статистики, сначала вызовите calculate()")
        mean_v = np.mean(values)
        median_v = np.median(values)
        mode_res = stats.mode(values, keepdims=False)
        # mode_res.mode может быть массивом или скаляр
        mode_v = mode_res.mode
        if hasattr(mode_v, "__len__"):
            mode_v = mode_v[0]
        var_v = np.var(values)
        std_v = np.std(values)
        return {
            'mean': mean_v,
            'median': median_v,
            'mode': mode_v,
            'variance': var_v,
            'std': std_v
        }
