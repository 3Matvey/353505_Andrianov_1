import matplotlib.pyplot as plt

def plot_series_vs_analytic(series_results, filename=None):
    x = [res['x'] for res in series_results]
    fx = [res['F(x)'] for res in series_results]
    fx_analytic = [res['Math F(x)'] for res in series_results]
    plt.figure(figsize=(10, 6))
    plt.plot(x, fx, label='Сумма ряда', color='blue')
    plt.plot(x, fx_analytic, label='Аналитическая функция', color='red', linestyle='--')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Сравнение суммы ряда и аналитической функции')
    plt.legend()
    plt.grid(True)
    plt.annotate('eps = |F(x) - Math F(x)|', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=10, color='gray')
    if filename:
        plt.savefig(filename)
    plt.show() 