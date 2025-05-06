from .models import SeriesAnalyzer
from .utils import plot_series_vs_analytic
import numpy as np


def main():
    x_values = np.linspace(1.1, 3, 50)  # |x| > 1
    analyzer = SeriesAnalyzer(x_values, n_terms=50, eps=1e-6)
    analyzer.calculate()
    print('Статистика по F(x):', analyzer.get_statistics('F(x)'))
    print('Статистика по Math F(x):', analyzer.get_statistics('Math F(x)'))
    plot_series_vs_analytic(analyzer.series_results, filename='series_vs_analytic.png')


if __name__ == '__main__':
    main()    