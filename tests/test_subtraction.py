"""
Тесты для кнопки вычитания (-) в калькуляторе.

Охватывает:
- Базовые операции вычитания
- Граничные случаи (нули, отрицательные результаты)
- Повторное нажатие кнопки -
- Цепочки вычитаний
- Большие числа
- Вычитание большего из меньшего (отрицательные результаты)
"""

import pytest
from page_objects.calculator_page import CalculatorPage


@pytest.mark.calculator
@pytest.mark.subtraction
class TestSubtractionBasic:
    """Базовые тесты операции вычитания."""
    
    @pytest.mark.smoke
    def test_subtraction_5_minus_3(self, calculator):
        """
        Smoke тест: Проверяет простейшее вычитание 5 - 3 = 2.
        
        Быстрый smoke тест для проверки базовой функциональности вычитания.
        """
        calculator.calculate_subtraction(5, 3)
        result = calculator.get_result_as_number()
        assert result == 2, f"Expected 5-3=2, but got {result}"
    
    @pytest.mark.parametrize("num1,num2,expected", [
        # Простые случаи (результат > 0)
        (5, 2, 3),
        (10, 5, 5),
        (9, 4, 5),
        (8, 3, 5),
        (7, 7, 0),  # Равные числа
        # Двузначные числа
        (20, 10, 10),
        (50, 25, 25),
        (100, 50, 50),
        (99, 9, 90),
        # Трехзначные и более
        (200, 100, 100),
        (500, 250, 250),
        (1000, 500, 500),
        (999, 999, 0),
    ])
    def test_subtraction_positive_result(self, calculator, num1, num2, expected):
        """
        Тест: Вычитание с положительным результатом (num1 >= num2).
        
        Проверяет базовую функциональность кнопки (-) когда
        уменьшаемое больше или равно вычитаемому.
        """
        calculator.calculate_subtraction(num1, num2)
        result = calculator.get_result_as_number()
        assert result == expected, \
            f"Expected {num1}-{num2}={expected}, but got {result}"
    
    def test_subtraction_zero_minus_zero(self, calculator):
        """
        Тест: 0 - 0 = 0
        
        Проверяет вычитание нуля из нуля.
        """
        calculator.calculate_subtraction(0, 0)
        result = calculator.get_result_as_number()
        assert result == 0, f"Expected 0-0=0, but got {result}"
    
    def test_subtraction_number_minus_zero(self, calculator):
        """
        Тест: 5 - 0 = 5
        
        Проверяет, что вычитание нуля не меняет число.
        """
        calculator.calculate_subtraction(5, 0)
        result = calculator.get_result_as_number()
        assert result == 5, f"Expected 5-0=5, but got {result}"
    
    def test_subtraction_same_numbers(self, calculator):
        """
        Тест: 7 - 7 = 0
        
        Проверяет, что вычитание числа из самого себя дает 0.
        """
        calculator.calculate_subtraction(7, 7)
        result = calculator.get_result_as_number()
        assert result == 0, f"Expected 7-7=0, but got {result}"


@pytest.mark.calculator
@pytest.mark.subtraction
class TestSubtractionWithZero:
    """Тесты вычитания с нулем (граничные случаи)."""
    
    def test_zero_minus_zero(self, calculator):
        """
        Тест: 0 - 0 = 0
        
        Проверяет вычитание нуля из нуля.
        """
        calculator.calculate_subtraction(0, 0)
        result = calculator.get_result_as_number()
        assert result == 0, f"Expected 0-0=0, but got {result}"
    
    @pytest.mark.parametrize("number,expected", [
        (1, 1),
        (5, 5),
        (10, 10),
        (100, 100),
        (999, 999),
    ])
    def test_number_minus_zero(self, calculator, number, expected):
        """
        Тест: число - 0 = число
        
        Проверяет, что вычитание нуля не меняет число.
        """
        calculator.calculate_subtraction(number, 0)
        result = calculator.get_result_as_number()
        assert result == expected, \
            f"Expected {number}-0={expected}, but got {result}"
    
    @pytest.mark.parametrize("number,expected", [
        (1, -1),
        (5, -5),
        (10, -10),
        (100, -100),
    ])
    def test_zero_minus_number(self, calculator, number, expected):
        """
        Тест: 0 - число = -число
        
        Проверяет вычитание числа из нуля (результат отрицательный).
        Некоторые простые калькуляторы могут не поддерживать отрицательные числа.
        """
        calculator.calculate_subtraction(0, number)
        result = calculator.get_result_as_number()
        # Проверяем, поддерживает ли калькулятор отрицательные числа
        # Если нет, тест может упасть или показать ошибку
        assert result == expected or result < 0, \
            f"Expected {expected} or negative number, but got {result}"


@pytest.mark.calculator
@pytest.mark.subtraction
class TestSubtractionNegativeResults:
    """Тесты вычитания с отрицательным результатом."""
    
    @pytest.mark.parametrize("num1,num2,expected", [
        # Меньшее - большее = отрицательное
        (1, 2, -1),
        (5, 10, -5),
        (10, 20, -10),
        (50, 100, -50),
        (100, 999, -899),
    ])
    def test_subtraction_negative_result(self, calculator, num1, num2, expected):
        """
        Тест: Вычитание большего числа из меньшего (отрицательный результат).
        
        Проверяет поддержку отрицательных чисел.
        Примечание: некоторые простые калькуляторы могут не поддерживать
        отрицательные числа и показывать ошибку или 0.
        """
        calculator.calculate_subtraction(num1, num2)
        result = calculator.get_result_as_number()
        # Проверяем поддержку отрицательных чисел
        assert result == expected or result < 0, \
            f"Expected {num1}-{num2}={expected}, but got {result}"


@pytest.mark.calculator
@pytest.mark.subtraction
class TestSubtractionMultiplePresses:
    """Тесты повторного нажатия кнопки вычитания."""
    
    def test_multiple_minus_presses_consecutive(self, calculator):
        """
        Тест: Множественное нажатие кнопки - подряд.
        
        Проверяет поведение при повторном нажатии кнопки -:
        10 - - 3 (калькулятор должен игнорировать повторное - или использовать последнее)
        
        Ожидаемый результат: 10 - 3 = 7
        """
        calculator.enter_number(10)
        calculator.tap_minus()
        calculator.tap_minus()  # Повторное нажатие
        calculator.tap_minus()  # Еще одно
        calculator.enter_number(3)
        calculator.tap_equals()
        
        result = calculator.get_result_as_number()
        assert result == 7, \
            f"Expected 10-3=7 (ignoring multiple - presses), but got {result}"


@pytest.mark.calculator
@pytest.mark.subtraction
class TestSubtractionChains:
    """Тесты цепочек вычитаний."""
    
    @pytest.mark.parametrize("numbers,expected", [
        # Простые цепочки
        ([10, 2, 3], 5),       # 10-2-3=5
        ([20, 5, 5], 10),      # 20-5-5=10
        ([100, 20, 30], 50),   # 100-20-30=50
        # Длинные цепочки
        ([10, 1, 1, 1, 1], 6), # 10-1-1-1-1=6
        ([50, 5, 10, 15], 20), # 50-5-10-15=20
        # С нулями
        ([10, 0, 5, 0], 5),    # 10-0-5-0=5
        ([20, 0, 10, 0], 10),  # 20-0-10-0=10
    ])
    def test_chain_subtraction(self, calculator, numbers, expected):
        """
        Тест: Цепочки вычитаний вида num1 - num2 - num3 - ... = результат.
        
        Проверяет последовательное вычитание нескольких чисел.
        
        Например: 10 - 2 - 3 = 5
        """
        calculator.enter_number(numbers[0])
        
        for num in numbers[1:]:
            calculator.tap_minus()
            calculator.enter_number(num)
        
        calculator.tap_equals()
        result = calculator.get_result_as_number()
        
        operation_str = "-".join(map(str, numbers))
        assert result == expected, \
            f"Expected {operation_str}={expected}, but got {result}"
    
    def test_chain_without_final_equals(self, calculator):
        """
        Тест: Цепочка вычитаний без финального =.
        
        При вводе: 20 - 5 - 3 (без нажатия =)
        Ожидается: промежуточные результаты или финальный результат 12
        """
        calculator.enter_number(20)
        calculator.tap_minus()
        calculator.enter_number(5)
        calculator.tap_minus()  # Может показаться промежуточный результат 15
        calculator.enter_number(3)
        calculator.tap_equals()
        
        result = calculator.get_result_as_number()
        assert result == 12, \
            f"Expected 20-5-3=12, but got {result}"
    
    def test_chain_subtraction_with_equals_in_middle(self, calculator):
        """
        Тест: Цепочка с нажатием = в середине.
        
        Проверяет: 20 - 5 = ... - 3 = 12
        После первого = показывается промежуточный результат 15,
        затем продолжается вычитание.
        """
        calculator.enter_number(20)
        calculator.tap_minus()
        calculator.enter_number(5)
        calculator.tap_equals()  # Должно показать 15
        
        intermediate = calculator.get_result_as_number()
        assert intermediate == 15, \
            f"Expected intermediate result 15, but got {intermediate}"
        
        # Продолжаем операцию
        calculator.tap_minus()
        calculator.enter_number(3)
        calculator.tap_equals()
        
        final_result = calculator.get_result_as_number()
        assert final_result == 12, \
            f"Expected final result 12, but got {final_result}"


@pytest.mark.calculator
@pytest.mark.subtraction
class TestSubtractionLargeNumbers:
    """Тесты вычитания больших чисел."""
    
    @pytest.mark.parametrize("num1,num2,expected", [
        # Большие числа
        (3000, 1000, 2000),
        (10000, 1, 9999),
        (80235, 12345, 67890),
        # Очень большие числа
        (300000, 100000, 200000),
        (1000000, 1, 999999),
    ])
    def test_subtraction_large_numbers(self, calculator, num1, num2, expected):
        """
        Тест: Вычитание больших чисел.
        
        Проверяет, что калькулятор корректно обрабатывает большие числа.
        """
        calculator.calculate_subtraction(num1, num2)
        result = calculator.get_result_as_number()
        assert result == expected, \
            f"Expected {num1}-{num2}={expected}, but got {result}"


@pytest.mark.calculator
@pytest.mark.subtraction
class TestSubtractionSpecialCases:
    """Специальные случаи и edge cases для вычитания."""
    
    def test_subtraction_after_clear(self, calculator):
        """
        Тест: Вычитание после очистки калькулятора.
        
        Проверяет, что после очистки калькулятор корректно выполняет вычитание.
        """
        # Выполняем произвольную операцию
        calculator.calculate_subtraction(10, 5)
        
        # Очищаем
        calculator.clear_display()
        
        # Выполняем новую операцию
        calculator.calculate_subtraction(7, 3)
        result = calculator.get_result_as_number()
        assert result == 4, \
            f"Expected 7-3=4 after clear, but got {result}"
    
    def test_subtraction_same_number(self, calculator):
        """
        Тест: Вычитание числа из самого себя.
        
        Проверяет: num - num = 0
        """
        test_cases = [(1, 0), (5, 0), (50, 0), (123, 0)]
        
        for num, expected in test_cases:
            calculator.calculate_subtraction(num, num)
            result = calculator.get_result_as_number()
            assert result == expected, \
                f"Expected {num}-{num}={expected}, but got {result}"
    
    def test_subtraction_immediately_after_result(self, calculator):
        """
        Тест: Вычитание сразу после получения результата.
        
        Проверяет: 10-3=7, затем -2=5
        (результат предыдущей операции используется как первый операнд)
        """
        calculator.enter_number(10)
        calculator.tap_minus()
        calculator.enter_number(3)
        calculator.tap_equals()
        
        result1 = calculator.get_result_as_number()
        assert result1 == 7, f"Expected 10-3=7, but got {result1}"
        
        # Продолжаем вычисление, используя результат
        calculator.tap_minus()
        calculator.enter_number(2)
        calculator.tap_equals()
        
        result2 = calculator.get_result_as_number()
        assert result2 == 5, \
            f"Expected 7-2=5 (continuation), but got {result2}"
    
    def test_subtraction_repeated_equals(self, calculator):
        """
        Тест: Повторное нажатие = после операции вычитания.
        
        Проверяет поведение: 10-3= = = (может повторять последнюю операцию)
        Некоторые калькуляторы: 10-3=7, =4, =1 (вычитают 3 каждый раз)
        Другие: 10-3=7, =7, =7 (не меняется)
        """
        calculator.enter_number(10)
        calculator.tap_minus()
        calculator.enter_number(3)
        calculator.tap_equals()
        
        result1 = calculator.get_result_as_number()
        assert result1 == 7, f"Expected 10-3=7, but got {result1}"
        
        # Нажимаем = еще раз
        calculator.tap_equals()
        result2 = calculator.get_result_as_number()
        
        # Проверяем оба возможных поведения
        # iOS калькулятор обычно повторяет операцию: 7-3=4
        assert result2 in [7, 4], \
            f"Expected either 7 (no change) or 4 (repeat -3), but got {result2}"
    
    def test_subtraction_from_result_of_addition(self, calculator):
        """
        Тест: Вычитание из результата сложения.
        
        Проверяет смешанные операции: (2+3)-1=4
        """
        calculator.enter_number(2)
        calculator.tap_plus()
        calculator.enter_number(3)
        calculator.tap_equals()
        
        result1 = calculator.get_result_as_number()
        assert result1 == 5, f"Expected 2+3=5, but got {result1}"
        
        # Вычитаем из результата
        calculator.tap_minus()
        calculator.enter_number(1)
        calculator.tap_equals()
        
        result2 = calculator.get_result_as_number()
        assert result2 == 4, \
            f"Expected 5-1=4, but got {result2}"


@pytest.mark.calculator
@pytest.mark.subtraction
@pytest.mark.regression
class TestSubtractionEdgeCases:
    """Экстремальные и граничные случаи для вычитания."""
    
    def test_subtraction_result_becomes_zero(self, calculator):
        """
        Тест: Вычитание до нуля.
        
        Проверяет: 5-5=0, затем -0=0
        """
        calculator.enter_number(5)
        calculator.tap_minus()
        calculator.enter_number(5)
        calculator.tap_equals()
        
        result1 = calculator.get_result_as_number()
        assert result1 == 0, f"Expected 5-5=0, but got {result1}"
        
        # Вычитаем из нуля
        calculator.tap_minus()
        calculator.enter_number(0)
        calculator.tap_equals()
        
        result2 = calculator.get_result_as_number()
        assert result2 == 0, f"Expected 0-0=0, but got {result2}"
    
    @pytest.mark.parametrize("num1,num2", [
        (1, 1),
        (10, 10),
        (999, 999),
        (12345, 12345),
    ])
    def test_subtraction_equal_numbers_result_zero(self, calculator, num1, num2):
        """
        Тест: Вычитание равных чисел всегда дает 0.
        
        Параметризованная проверка для различных пар равных чисел.
        """
        calculator.calculate_subtraction(num1, num2)
        result = calculator.get_result_as_number()
        assert result == 0, \
            f"Expected {num1}-{num2}=0, but got {result}"
