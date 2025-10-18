"""
Пример тестов для приложения Калькулятор.

Демонстрирует:
- Использование fixture calculator (возвращает CalculatorPage)
- Page Object Pattern
- Базовые математические операции
- Проверки результатов
"""

import pytest
import allure
from page_objects.calculator_page import CalculatorPage
from utils.device_manager import DeviceManager


@allure.feature("Calculator Basic Operations")
@allure.story("Basic Arithmetic")
class TestCalculatorBasic:
    """Базовые тесты калькулятора."""
    
    @allure.title("Test addition 2 + 3 = 5")
    @allure.severity(allure.severity_level.NORMAL)
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
    
    @allure.title("Test addition using high-level method")
    @allure.severity(allure.severity_level.NORMAL)
    def test_addition_using_high_level_method(self, calculator):
        """
        Тест: Проверяет сложение 2 + 3 = 5 используя высокоуровневый метод.
        """
        # Act
        calculator.calculate_addition(2, 3)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 5, f"Expected 5, but got {result}"
    
    @allure.title("Test addition 10 + 20 = 30")
    @allure.severity(allure.severity_level.NORMAL)
    def test_addition_10_plus_20(self, calculator):
        """
        Тест: Проверяет сложение многозначных чисел 10 + 20 = 30
        """
        # Act
        calculator.calculate_addition(10, 20)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 30, f"Expected 30, but got {result}"
    
    @allure.title("Test subtraction 5 - 3 = 2")
    @allure.severity(allure.severity_level.NORMAL)
    def test_subtraction(self, calculator):
        """
        Тест: Проверяет вычитание 10 - 3 = 7
        """
        # Act
        calculator.calculate_subtraction(10, 3)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 7, f"Expected 7, but got {result}"
    
    @allure.title("Test multiplication 4 × 5 = 20")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiplication(self, calculator):
        """
        Тест: Проверяет умножение 4 × 5 = 20
        """
        # Act
        calculator.calculate_multiplication(4, 5)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 20, f"Expected 20, but got {result}"
    
    @allure.title("Test division 10 ÷ 2 = 5")
    @allure.severity(allure.severity_level.NORMAL)
    def test_division(self, calculator):
        """
        Тест: Проверяет деление 15 ÷ 3 = 5
        """
        # Act
        calculator.calculate_division(15, 3)
        
        # Assert
        result = calculator.get_result_as_number()
        assert result == 5, f"Expected 5, but got {result}"
    
    @allure.title("Test chain operations 2 + 3 - 1 = 4")
    @allure.severity(allure.severity_level.NORMAL)
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
    
    @allure.title("Test clear button functionality")
    @allure.severity(allure.severity_level.NORMAL)
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


@allure.feature("Calculator Smoke Tests")
@allure.story("Smoke Tests")
@pytest.mark.smoke
class TestCalculatorSmoke:
    """Smoke тесты калькулятора."""
    
    @allure.title("Test calculator is opened")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_calculator_is_opened(self, calculator):
        """
        Smoke test: Проверяет, что калькулятор успешно открыт
        """
        assert calculator.is_calculator_opened(), \
            "Calculator app is not opened"
    
    @allure.title("Test basic addition works")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_basic_addition_works(self, calculator):
        """
        Smoke test: Базовая проверка работоспособности калькулятора
        """
        calculator.calculate_addition(1, 1)
        result = calculator.get_result_as_number()
        assert result == 2, f"Basic addition failed: 1+1 != {result}"


@allure.feature("Calculator Edge Cases")
@allure.story("Edge Cases")
@pytest.mark.regression
class TestCalculatorEdgeCases:
    """Тесты граничных случаев."""
    
    @allure.title("Test addition with zero")
    @allure.severity(allure.severity_level.NORMAL)
    def test_addition_with_zero(self, calculator):
        """
        Тест: Сложение с нулем 5 + 0 = 5
        """
        calculator.calculate_addition(5, 0)
        result = calculator.get_result_as_number()
        assert result == 5, f"Expected 5, but got {result}"
    
    @allure.title("Test multiplication by zero")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiplication_by_zero(self, calculator):
        """
        Тест: Умножение на ноль 5 × 0 = 0
        """
        calculator.calculate_multiplication(5, 0)
        result = calculator.get_result_as_number()
        assert result == 0, f"Expected 0, but got {result}"
    
    @allure.title("Test addition parametrized: {num1} + {num2} = {expected}")
    @allure.severity(allure.severity_level.NORMAL)
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


@allure.feature("Device Features")
@allure.story("Device Management")
@pytest.mark.device_features
class TestDeviceManagerFeatures:
    """Тесты для демонстрации возможностей DeviceManager."""
    
    @allure.title("Test app restart")
    @allure.severity(allure.severity_level.NORMAL)
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
    
    @allure.title("Test landscape orientation display")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.android
    def test_landscape_orientation_display(self, calculator, device_manager):
        """
        Тест: Проверяет отображение интерфейса калькулятора в пейзажной ориентации.
        
        Выполняет следующие проверки:
        1. Приложение запускается в портретной ориентации (fixture гарантирует)
        2. Выполняется операция в портретной ориентации
        3. Запоминаются координаты ключевых кнопок в портретной ориентации
        4. Переключается в пейзажную ориентацию
        5. Проверяется доступность основных элементов UI
        6. Проверяется изменение размера экрана (ширина > высоты в landscape)
        7. Проверяется значительное изменение координат кнопок (подтверждение смены ориентации)
        8. Проверяется сохранение результата после смены ориентации
        9. Выполняется новая операция в пейзажной ориентации
        
        Note: Этот тест работает только на Android (iOS Simulator не поддерживает смену ориентации программно)
        """
        # Пропускаем тест если платформа не Android
        if device_manager.platform != "android":
            pytest.skip("Test requires Android platform")
        
        # Шаг 1: Проверяем текущую ориентацию (должна быть портретная)
        assert device_manager.is_portrait(), \
            "Test should start in PORTRAIT orientation"
        
        # Шаг 2: Выполняем операцию в портретной ориентации
        result_portrait = calculator.calculate_addition(3, 7)
        assert result_portrait == "10", f"Expected 3+7=10, got {result_portrait}"
        
        # Шаг 2.1: Запоминаем координаты ключевых кнопок в портретной ориентации
        button_5_portrait = calculator._find_element('5')
        button_equals_portrait = calculator._find_element('equals')
        
        coords_portrait = {
            'button_5': button_5_portrait.location,
            'button_equals': button_equals_portrait.location,
            'screen_size': device_manager.driver.get_window_size()
        }
        
        # Шаг 3: Переключаемся в пейзажную ориентацию (с ожиданием перестройки UI)
        device_manager.rotate_to_landscape()
        
        # Шаг 4: Проверяем доступность основных элементов UI в пейзажной ориентации
        assert calculator.is_calculator_opened(), \
            "Calculator UI should be accessible in landscape orientation"
        
        # Шаг 4.1: Проверяем координаты кнопок в пейзажной ориентации
        button_5_landscape = calculator._find_element('5')
        button_equals_landscape = calculator._find_element('equals')
        
        coords_landscape = {
            'button_5': button_5_landscape.location,
            'button_equals': button_equals_landscape.location,
            'screen_size': device_manager.driver.get_window_size()
        }
        
        # Проверяем, что размер экрана изменился (ширина и высота поменялись местами)
        portrait_width = coords_portrait['screen_size']['width']
        portrait_height = coords_portrait['screen_size']['height']
        landscape_width = coords_landscape['screen_size']['width']
        landscape_height = coords_landscape['screen_size']['height']
        
        assert landscape_width > landscape_height, \
            f"In landscape mode width should be > height, got {landscape_width}x{landscape_height}"
        assert portrait_width < portrait_height, \
            f"In portrait mode width should be < height, got {portrait_width}x{portrait_height}"
        
        # Проверяем, что координаты кнопок значительно изменились
        button_5_moved = (
            abs(coords_portrait['button_5']['x'] - coords_landscape['button_5']['x']) > 50 or
            abs(coords_portrait['button_5']['y'] - coords_landscape['button_5']['y']) > 50
        )
        button_equals_moved = (
            abs(coords_portrait['button_equals']['x'] - coords_landscape['button_equals']['x']) > 50 or
            abs(coords_portrait['button_equals']['y'] - coords_landscape['button_equals']['y']) > 50
        )
        
        assert button_5_moved, \
            f"Button '5' should move significantly after orientation change. " \
            f"Portrait: {coords_portrait['button_5']}, Landscape: {coords_landscape['button_5']}"
        
        assert button_equals_moved, \
            f"Button 'equals' should move significantly after orientation change. " \
            f"Portrait: {coords_portrait['button_equals']}, Landscape: {coords_landscape['button_equals']}"
        
        # Шаг 5: Проверяем, что результат сохранился после смены ориентации
        result_landscape = calculator.get_result()
        assert result_landscape == "10", \
            f"Result should persist after orientation change, expected 10, got {result_landscape}"
        
        # Шаг 6: Выполняем новую операцию в пейзажной ориентации
        result_landscape_calc = calculator.calculate_addition(5, 5)
        assert result_landscape_calc == "10", \
            f"Calculator should work in landscape orientation, expected 5+5=10, got {result_landscape_calc}"
        
        # Teardown: Возвращаем портретную ориентацию (fixture сделает это автоматически в следующем тесте)
        device_manager.rotate_to_portrait(wait_for_ui=False)
    
    @allure.title("Test scientific calculator mode in landscape orientation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.android
    def test_landscape_scientific_mode(self, calculator, device_manager):
        """
        Тест: Проверяет наличие инженерных кнопок в пейзажной ориентации.
        
        Проверяет, что:
        1. В портретной ориентации научные кнопки недоступны
        2. В пейзажной ориентации появляются научные кнопки (sin, cos, sqrt, π, e)
        
        Note: Работает только на Android с Samsung Calculator
        """
        if device_manager.platform != "android":
            pytest.skip("Test requires Android platform")
        
        # Шаг 1: Проверяем отсутствие научных кнопок в portrait
        assert device_manager.is_portrait(), "Test should start in PORTRAIT orientation"
        
        scientific_buttons = ['sin', 'cos', 'sqrt', 'pi', 'e']
        for button in scientific_buttons:
            assert not calculator.is_button_visible(button, timeout=1), \
                f"Scientific button '{button}' should not be available in portrait mode"
        
        # Шаг 2: Переключаемся в пейзажную ориентацию (с ожиданием перестройки UI)
        device_manager.rotate_to_landscape()
        
        # Шаг 3: Проверяем наличие научных кнопок в landscape
        found_buttons = [btn for btn in scientific_buttons if calculator.is_button_visible(btn)]
        
        # Проверяем, что найдено минимум 3 научные кнопки
        assert len(found_buttons) >= 3, \
            f"Expected at least 3 scientific buttons in landscape mode, but found only {len(found_buttons)}: {found_buttons}"
        
        # Teardown
        device_manager.rotate_to_portrait(wait_for_ui=False)
    
    @allure.title("Test background app")
    @allure.severity(allure.severity_level.NORMAL)
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
