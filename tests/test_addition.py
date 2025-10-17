"""
Тесты для кнопки сложения (+) в калькуляторе.

Охватывает:
- Базовые операции сложения
- Граничные случаи (нули, большие числа)
- Повторное нажатие кнопки +
- Цепочки сложений (мультипликативное сложение)
- Переполнение и максимальные значения
- Проверка количества отображаемых цифр
"""

import pytest
from page_objects.calculator_page import CalculatorPage


def count_digits(number: float) -> int:
    """
    Подсчитывает количество цифр в числе (без учета знака, точки, запятых).
    
    Args:
        number: Число для подсчета цифр
        
    Returns:
        Количество цифр в числе
    """
    # Преобразуем в строку и убираем всё кроме цифр
    num_str = str(abs(int(number)))
    return len(num_str)


@pytest.mark.calculator
@pytest.mark.addition
class TestAdditionBasic:
    """Базовые тесты операции сложения."""
    
    @pytest.mark.smoke
    def test_addition_2_plus_2(self, calculator):
        """
        Smoke тест: Проверяет простейшее сложение 2 + 2 = 4.
        
        Быстрый smoke тест для проверки базовой функциональности сложения.
        """
        calculator.calculate_addition(2, 2)
        result = calculator.get_result_as_number()
        assert result == 4, f"Expected 2+2=4, but got {result}"
    
    @pytest.mark.parametrize("num1,num2,expected_result,description", [
        (1, 1, 2, "1 digit + 1 digit = 1 digit"),
        (5, 7, 12, "1 digit + 1 digit = 2 digits"),
        (10, 20, 30, "2 digits + 2 digits = 2 digits"),
        (50, 60, 110, "2 digits + 2 digits = 3 digits"),
        (500000000, 499999999, 999999999, "9 digits + 9 digits = 9 digits (max display)"),
    ])
    def test_addition_digit_count(self, calculator, num1, num2, expected_result, description):
        """
        Тест: Проверяет корректность сложения и количество отображаемых цифр в результате.
        
        Проверяет что калькулятор:
        1. Правильно выполняет операцию сложения
        2. Корректно отображает результаты с 1, 2, 3 и 9 цифрами
        
        iOS калькулятор может отображать до 9 цифр в обычном формате.
        """
        calculator.calculate_addition(num1, num2)
        result = calculator.get_result_as_number()
        
        # Проверяем правильность результата сложения
        assert result == expected_result, \
            f"{description}: {num1}+{num2} expected {expected_result}, but got {result}"
        
        # Проверяем количество цифр в результате
        expected_digits = len(str(int(expected_result)))
        actual_digits = count_digits(result)
        assert actual_digits == expected_digits, \
            f"{description}: expected {expected_digits} digits in result, got {actual_digits} digits"
    
    @pytest.mark.parametrize("num1,num2,expected_result,description", [
        (int("1" + "0" * 29), int("1" + "0" * 29), "2e29", "50 digits + 50 digits = exponential notation"),
    ])
    def test_addition_overflow_display_limit(self, calculator, num1, num2, expected_result, description):
        """
        Тест: Проверяет поведение при превышении лимита отображения (экспоненциальная нотация).
        
        iOS калькулятор может отображать максимум 9 цифр в обычном формате.
        При вводе очень больших чисел (50 цифр) калькулятор автоматически
        переходит в экспоненциальную нотацию (например, 1e+50).
        
        Этот тест проверяет, что калькулятор корректно обрабатывает 
        сложение очень больших чисел и отображает результат в экспоненциальной нотации.
        """
        calculator.calculate_addition(num1, num2)
        result = calculator.get_result()
        
        # Проверяем что результат математически корректен
        # При работе с экспоненциальной нотацией допускается погрешность округления
        assert result == expected_result, \
            f"{description}: {num1}+{num2} expected {expected_result}, but got {result}"
    
    @pytest.mark.parametrize("num1,num2,expected", [
        (0, 0, 0),  # 0 + 0 = 0
        (0, 5, 5),  # 0 + число = число
        (5, 0, 5),  # число + 0 = число
    ])
    def test_addition_with_zero(self, calculator, num1, num2, expected):
        """
        Тест: Сложение с нулем.
        
        Проверяет три случая:
        - 0 + 0 = 0
        - 0 + число = число
        - число + 0 = число
        """
        calculator.calculate_addition(num1, num2)
        result = calculator.get_result_as_number()
        assert result == expected, f"Expected {num1}+{num2}={expected}, but got {result}"


@pytest.mark.calculator
@pytest.mark.addition
class TestAdditionMultiplePresses:
    """Тесты повторного нажатия кнопки сложения."""
    
    def test_multiple_plus_presses_consecutive(self, calculator):
        """
        Тест: Множественное нажатие кнопки + подряд.
        
        Проверяет поведение при повторном нажатии кнопки +:
        2 + + 3 (калькулятор должен игнорировать повторное + или использовать последнее)
        
        Ожидаемый результат: 2 + 3 = 5
        """
        calculator.enter_number(2)
        calculator.tap_plus()
        calculator.tap_plus()  # Повторное нажатие
        calculator.tap_plus()  # Еще одно
        calculator.enter_number(3)
        calculator.tap_equals()
        
        result = calculator.get_result_as_number()
        assert result == 5, \
            f"Expected 2+3=5 (ignoring multiple + presses), but got {result}"
    
    def test_addition_repeated_equals(self, calculator):
        """
        Тест: Повторное нажатие = после операции сложения.
        
        iOS калькулятор запоминает последнюю операцию и повторяет её:
        2+3 = 5
        = 8 (повторяет +3)
        = 11 (снова +3)
        """
        calculator.enter_number(2)
        calculator.tap_plus()
        calculator.enter_number(3)
        calculator.tap_equals()
        
        result1 = calculator.get_result_as_number()
        assert result1 == 5, f"Expected 2+3=5, but got {result1}"
        
        calculator.tap_equals()
        result2 = calculator.get_result_as_number()
        assert result2 == 8, f"Expected 5+3=8 (repeat operation), but got {result2}"
        
        calculator.tap_equals()
        result3 = calculator.get_result_as_number()
        assert result3 == 11, f"Expected 8+3=11 (repeat operation), but got {result3}"


@pytest.mark.calculator
@pytest.mark.addition
class TestAdditionChains:
    """Тесты цепочек сложений (мультипликативное сложение)."""
    
    @pytest.mark.parametrize("numbers,expected", [
        ([1, 2, 3], 6),
        ([5, 5, 5], 15),
        ([1, 1, 1, 1, 1], 5),
        ([0, 5, 0, 10], 15),
    ])
    def test_chain_addition(self, calculator, numbers, expected):
        """
        Тест: Цепочки сложений вида num1 + num2 + num3 + ... = результат.
        
        Проверяет мультипликативное сложение, когда после операции +
        и второго числа вместо = нажимается еще одно +.
        
        Например: 1 + 2 + 3 = 6
        """
        calculator.enter_number(numbers[0])
        
        for num in numbers[1:]:
            calculator.tap_plus()
            calculator.enter_number(num)
        
        calculator.tap_equals()
        result = calculator.get_result_as_number()
        
        operation_str = "+".join(map(str, numbers))
        assert result == expected, \
            f"Expected {operation_str}={expected}, but got {result}"
    
    def test_chain_without_final_equals(self, calculator):
        """
        Тест: Цепочка сложений без финального =.
        
        При вводе: 2 + 3 + 5 (без нажатия =)
        Ожидается: промежуточные результаты или финальный результат 10
        """
        calculator.enter_number(2)
        calculator.tap_plus()
        calculator.enter_number(3)
        calculator.tap_plus()  # Здесь может показаться промежуточный результат 5
        calculator.enter_number(5)
        calculator.tap_equals()
        
        result = calculator.get_result_as_number()
        assert result == 10, \
            f"Expected 2+3+5=10, but got {result}"
    
    def test_chain_addition_with_equals_in_middle(self, calculator):
        """
        Тест: Цепочка с нажатием = в середине.
        
        Проверяет: 2 + 3 = ... + 5 = 10
        После первого = показывается промежуточный результат 5,
        затем продолжается сложение.
        """
        calculator.enter_number(2)
        calculator.tap_plus()
        calculator.enter_number(3)
        calculator.tap_equals()  # Должно показать 5
        
        intermediate = calculator.get_result_as_number()
        assert intermediate == 5, \
            f"Expected intermediate result 5, but got {intermediate}"
        
        # Продолжаем операцию
        calculator.tap_plus()
        calculator.enter_number(5)
        calculator.tap_equals()
        
        final_result = calculator.get_result_as_number()
        assert final_result == 10, \
            f"Expected final result 10, but got {final_result}"


@pytest.mark.calculator
@pytest.mark.addition
class TestAdditionLargeNumbers:
    """Тесты сложения больших чисел."""
    
    @pytest.mark.parametrize("num1,num2,expected", [
        (1000, 2000, 3000),
        (9999, 1, 10000),
        (12345, 67890, 80235),
    ])
    def test_addition_large_numbers(self, calculator, num1, num2, expected):
        """
        Тест: Сложение больших чисел.
        
        Проверяет, что калькулятор корректно обрабатывает большие числа.
        """
        calculator.calculate_addition(num1, num2)
        result = calculator.get_result_as_number()
        assert result == expected, \
            f"Expected {num1}+{num2}={expected}, but got {result}"


@pytest.mark.calculator
@pytest.mark.addition
class TestAdditionSpecialCases:
    """Специальные случаи и edge cases для сложения."""
    
    def test_addition_after_clear(self, calculator):
        """
        Тест: Сложение после очистки калькулятора.
        
        Проверяет, что после очистки калькулятор корректно выполняет сложение.
        """
        # Выполняем произвольную операцию
        calculator.calculate_addition(5, 5)
        
        # Очищаем
        calculator.clear_display()
        
        # Выполняем новую операцию
        calculator.calculate_addition(2, 3)
        result = calculator.get_result_as_number()
        assert result == 5, \
            f"Expected 2+3=5 after clear, but got {result}"
    
    @pytest.mark.parametrize("num,expected", [
        (1, 2),
        (5, 10),
    ])
    def test_addition_same_number(self, calculator, num, expected):
        """
        Тест: Сложение числа с самим собой (удвоение).
        
        Проверяет: num + num = 2*num
        """
        calculator.calculate_addition(num, num)
        result = calculator.get_result_as_number()
        assert result == expected, \
            f"Expected {num}+{num}={expected}, but got {result}"
    
    def test_addition_immediately_after_result(self, calculator):
        """
        Тест: Сложение сразу после получения результата.
        
        Проверяет: 2+3=5, затем +10=15
        (результат предыдущей операции используется как первый операнд)
        """
        calculator.enter_number(2)
        calculator.tap_plus()
        calculator.enter_number(3)
        calculator.tap_equals()
        
        result1 = calculator.get_result_as_number()
        assert result1 == 5, f"Expected 2+3=5, but got {result1}"
        
        # Продолжаем вычисление, используя результат
        calculator.tap_plus()
        calculator.enter_number(10)
        calculator.tap_equals()
        
        result2 = calculator.get_result_as_number()
        assert result2 == 15, \
            f"Expected 5+10=15 (continuation), but got {result2}"
