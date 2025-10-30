import math
def calculate_function(x):
    try:
        return x**2 - math.exp(x)
    except OverflowError:
        return float('-inf')  # exp(x) → ∞ ⇒ f(x) → -∞


def find_characteristic_point(x0, h, target_value=-10, max_iterations=10000):
    if h <= 0:
        return {
            'success': False,
            'error': 'Шаг h должен быть положительным числом',
            'x': None,
            'y': None,
            'iterations': 0
        }

    x = x0
    iteration = 0

    y_prev = calculate_function(x)

    while iteration < max_iterations:
        x = x + h
        iteration += 1

        y = calculate_function(x)

        if (y_prev < target_value <= y) or (y_prev >= target_value > y):
            x_interp = x - h + h * (target_value - y_prev) / (y - y_prev)
            y_interp = target_value

            return {
                'success': True,
                'x': x_interp,
                'y': y_interp,
                'iterations': iteration,
                'message': f'Точка найдена: x = {x_interp:.6f}, y = {y_interp:.6f}'
            }

        y_prev = y

    return {
        'success': False,
        'error': f'Точка не найдена за {max_iterations} итераций',
        'x': x,
        'y': y_prev,
        'iterations': iteration
    }


def main():
    print("=" * 60)
    print("Поиск характерных точек функции f(x) = x² - e^x")
    print("Целевое значение: y = -10")
    print("=" * 60)

    try:
        x0 = float(input("\nВведите начальное значение X0: "))
        h = float(input("Введите шаг h (h > 0): "))

        max_iter_input = input("Введите максимальное количество итераций (Enter для 10000): ")
        max_iterations = int(max_iter_input) if max_iter_input else 10000

        result = find_characteristic_point(x0, h, -10, max_iterations)

        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТЫ:")
        print("=" * 60)

        if result['success']:
            print(f"✓ {result['message']}")
            print(f"  Количество итераций: {result['iterations']}")
        else:
            print(f"✗ {result['error']}")
            if result['x'] is not None:
                print(f"  Последнее значение: x = {result['x']:.6f}, y = {result['y']:.6f}")
                print(f"  Количество итераций: {result['iterations']}")

        print("=" * 60)

    except ValueError as e:
        print(f"\n✗ Ошибка ввода: {e}")
        print("Пожалуйста, вводите числовые значения.")
    except Exception as e:
        print(f"\n✗ Произошла ошибка: {e}")


if __name__ == "__main__":
    main()