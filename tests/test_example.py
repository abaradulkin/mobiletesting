"""
Пример тестов для приложения Калькулятор.

Демонстрирует:
- Использование fixture calculator (возвращает CalculatorPage)
- Page Object Pattern
- Базовые математические операции
- Проверки результатов
"""

import pytest
from page_objects.calculator_page import CalculatorPage
from utils.device_manager import DeviceManager


class TestCalculatorBasic:
    """Базовые тесты калькулятора."""
    
    def test_addition_2_plus_3(self, calculator):
        """
        Тест: Проверяет сложение 2 + 3 = 5
        
        Шаги:
        1. Ввести 2
        2. Нажать +
        3. Ввести 3
        4. Нажать =
        5. Проверить результат = 5
        """
        # Act
        calculator.enter_number(2)
        calculator.tap_plus()
        calculator.enter_number(3)
        calculator.tap_equals()
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 5, f"Expected 5, but got {result}"
    
    def test_addition_using_high_level_method(self, calculator):
        """
        Тест: Проверяет сложение 2 + 3 = 5 используя высокоуровневый метод.
        """
        # Act
        calculator.calculate_addition(2, 3)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 5, f"Expected 5, but got {result}"
    
    def test_addition_10_plus_20(self, calculator):
        """
        Тест: Проверяет сложение многозначных чисел 10 + 20 = 30
        """
        # Act
        calculator.calculate_addition(10, 20)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 30, f"Expected 30, but got {result}"
    
    def test_subtraction(self, calculator):
        """
        Тест: Проверяет вычитание 10 - 3 = 7
        """
        # Act
        calculator.calculate_subtraction(10, 3)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 7, f"Expected 7, but got {result}"
    
    def test_multiplication(self, calculator):
        """
        Тест: Проверяет умножение 4 × 5 = 20
        """
        # Act
        calculator.calculate_multiplication(4, 5)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 20, f"Expected 20, but got {result}"
    
    def test_division(self, calculator):
        """
        Тест: Проверяет деление 15 ÷ 3 = 5
        """
        # Act
        calculator.calculate_division(15, 3)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 5, f"Expected 5, but got {result}"
    
    def test_chain_operations(self, calculator):
        """
        Тест: Проверяет цепочку операций используя chain calling
        2 + 3 = 5
        """
        # Act
        calculator\
            .enter_number(2)\
            .tap_plus()\
            .enter_number(3)\
            .tap_equals()
        
        result = calculator.get_result_as_number()
        
        # Assert
        assert result == 5, f"Expected 5, but got {result}"
    
    def test_clear_button(self, calculator):
        """
        Тест: Проверяет функцию очистки калькулятора
        """
        # Arrange
        calculator.enter_number(123)
        
        # Act
        calculator.clear_display()
        result = calculator.get_result()
        
        # Assert
        # После очистки результат должен быть пустым или "0"
        assert result in ["", "0"], f"Expected empty or '0', but got {result}"


@pytest.mark.smoke
class TestCalculatorSmoke:
    """Smoke тесты калькулятора."""
    
    def test_calculator_is_opened(self, calculator):
        """
        Smoke test: Проверяет, что калькулятор успешно открыт
        """
        assert calculator.is_calculator_opened(), \
            "Calculator app is not opened"
    
    def test_basic_addition_works(self, calculator):
        """
        Smoke test: Базовая проверка работоспособности калькулятора
        """
        calculator.calculate_addition(1, 1)
        result = calculator.get_result_as_number()
        assert result == 2, f"Basic addition failed: 1+1 != {result}"


@pytest.mark.regression
class TestCalculatorEdgeCases:
    """Тесты граничных случаев."""
    
    def test_addition_with_zero(self, calculator):
        """
        Тест: Сложение с нулем 5 + 0 = 5
        """
        calculator.calculate_addition(5, 0)
        result = calculator.get_result_as_number()
        assert result == 5, f"Expected 5, but got {result}"
    
    def test_multiplication_by_zero(self, calculator):
        """
        Тест: Умножение на ноль 5 × 0 = 0
        """
        calculator.calculate_multiplication(5, 0)
        result = calculator.get_result_as_number()
        assert result == 0, f"Expected 0, but got {result}"
    
    @pytest.mark.parametrize("num1,num2,expected", [
        (1, 1, 2),
        (5, 5, 10),
        (9, 9, 18),
        (10, 10, 20),
    ])
    def test_addition_parametrized(self, calculator, num1, num2, expected):
        """
        Параметризованный тест: Проверяет различные комбинации сложения
        """
        calculator.calculate_addition(num1, num2)
        result = calculator.get_result_as_number()
        assert result == expected, \
            f"Expected {num1}+{num2}={expected}, but got {result}"


@pytest.mark.device_features
class TestDeviceManagerFeatures:
    """Тесты для демонстрации возможностей DeviceManager."""
    
    def test_app_restart(self, calculator, device_manager):
        """
        Тест: Проверяет перезапуск приложения
        """
        # Вводим данные
        calculator.enter_number(123)
        
        # Перезапускаем приложение
        device_manager.restart_app()
        
        # Проверяем, что приложение открыто и экран очищен
        assert calculator.is_calculator_opened(), \
            "Calculator not opened after restart"
        
        result = calculator.get_result()
        assert result in ["", "0"], \
            f"Display not cleared after restart, got: {result}"
    
    @pytest.mark.android
    def test_orientation_change(self, calculator, device_manager):
        """
        Тест: Проверяет работу калькулятора после смены ориентации
        
        Note: Этот тест работает только на Android
        """
        # Пропускаем тест если платформа не Android
        if device_manager.platform != "android":
            pytest.skip("Test requires Android platform")
        
        # Выполняем операцию
        result_before = calculator.calculate_addition(2, 3)
        assert result_before == "5"
        
        # Меняем ориентацию
        original_orientation = device_manager.driver.orientation
        device_manager.set_orientation('landscape')
        
        # Проверяем, что результат сохранился
        result_after = calculator.get_result()
        assert result_after == "5", \
            f"Result changed after orientation change: {result_after}"
        
        # Возвращаем исходную ориентацию
        device_manager.driver.orientation = original_orientation
    
    def test_background_app(self, calculator, device_manager):
        """
        Тест: Проверяет работу калькулятора после отправки в фон
        """
        # Выполняем операцию
        result_before = calculator.calculate_addition(2, 3)
        assert result_before == "5"
        
        # Отправляем в фон на 2 секунды
        device_manager.driver.background_app(2)
        
        # Проверяем, что результат сохранился
        result_after = calculator.get_result()
        assert result_after == "5", \
            f"Result changed after backgrounding: {result_after}"
