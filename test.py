import unittest
import math
from main import calculate_function, find_characteristic_point


class TestCalculateFunction(unittest.TestCase):

    def test_normal_values(self):
        """Тестирование обычных значений функции f(x) = x^2 - e^x"""
        self.assertAlmostEqual(calculate_function(0), -1.0, places=6)
        self.assertAlmostEqual(calculate_function(1), 1 - math.e, places=6)
        self.assertAlmostEqual(calculate_function(2), 4 - math.exp(2), places=6)

    def test_overflow_handling(self):
        """Тестирование обработки переполнения при больших x"""
        result = calculate_function(1000)
        self.assertEqual(result, float('-inf'))


class TestFindCharacteristicPoint(unittest.TestCase):

    def test_invalid_step_h(self):
        """Тест: h <= 0 → ошибка"""
        result = find_characteristic_point(x0=0, h=-0.1)
        self.assertFalse(result['success'])
        self.assertIn('Шаг h должен быть положительным', result['error'])

        result = find_characteristic_point(x0=0, h=0)
        self.assertFalse(result['success'])
        self.assertIn('Шаг h должен быть положительным', result['error'])

    def test_target_found_on_first_crossing(self):
        """Тест: пересечение целевого значения -10 между x=2.9 и x=3.0"""
        result = find_characteristic_point(x0=2.9, h=0.1, target_value=-10, max_iterations=10)
        self.assertTrue(result['success'])
        self.assertAlmostEqual(result['y'], -10.0, places=6)
        self.assertGreater(result['x'], 2.9)
        self.assertLess(result['x'], 3.0)
        self.assertEqual(result['iterations'], 1)

    def test_no_crossing_within_max_iterations(self):
        """Тест: не найдено пересечение за лимит итераций"""
        result = find_characteristic_point(x0=0, h=0.01, target_value=-10, max_iterations=5)
        self.assertFalse(result['success'])
        self.assertIn('Точка не найдена за 5 итераций', result['error'])
        self.assertEqual(result['iterations'], 5)
        self.assertAlmostEqual(result['x'], 0.05, places=6)

    def test_overflow_during_search(self):
        """Тест: переполнение exp(x) при больших x — функция возвращает -inf"""
        result = find_characteristic_point(x0=1000, h=1, target_value=-10, max_iterations=3)
        self.assertFalse(result['success'])
        self.assertIn('Точка не найдена за 3 итераций', result['error'])
        self.assertEqual(result['y'], float('-inf'))

    def test_negative_x0_with_eventual_crossing(self):
        """Тест: отрицательное x0, пересечение происходит позже"""
        result = find_characteristic_point(x0=-1, h=0.5, target_value=-10, max_iterations=10)
        self.assertTrue(result['success'])
        self.assertAlmostEqual(result['y'], -10.0, places=6)
        self.assertGreater(result['x'], 2.5)
        self.assertLess(result['x'], 3.0)
        # От -1 до 3.0 с шагом 0.5: 8 шагов (x = -0.5, 0, ..., 3.0 → 8 итераций)
        self.assertEqual(result['iterations'], 8)

    def test_no_crossing_when_both_below_target(self):
        """Тест: оба значения ниже -10 → нет пересечения"""
        result = find_characteristic_point(x0=3.0, h=0.1, target_value=-10, max_iterations=2)
        # f(3.0) ≈ -11.08, f(3.1) ≈ -12.58 → оба < -10 → нет перехода
        self.assertFalse(result['success'])
        self.assertIn('Точка не найдена за 2 итераций', result['error'])

    def test_interpolation_accuracy(self):
        """Тест: проверка формулы линейной интерполяции"""
        x_prev = 2.9
        y_prev = calculate_function(x_prev)
        y_curr = calculate_function(3.0)
        target = -10.0
        h = 0.1
        x_interp_expected = x_prev + h * (target - y_prev) / (y_curr - y_prev)
        result = find_characteristic_point(x0=2.9, h=0.1, target_value=-10, max_iterations=1)
        self.assertTrue(result['success'])
        self.assertAlmostEqual(result['x'], x_interp_expected, places=6)


if __name__ == '__main__':
    unittest.main()