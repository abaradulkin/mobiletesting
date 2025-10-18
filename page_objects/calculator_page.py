"""
Calculator Page Object для iOS и Android калькулятора.

Предоставляет методы для взаимодействия с калькулятором:
- Нажатие на цифры и операции
- Получение результата
- Очистка экрана
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
import logging
import allure

from utils.device_manager import DeviceManager

logger = logging.getLogger(__name__)


class CalculatorPage:
    """
    Page Object для приложения Калькулятор.
    
    Поддерживает iOS и Android платформы.
    """
    
    # Локаторы для iOS (используют accessibility id через name атрибут)
    IOS_LOCATORS = {
        # Цифры
        '0': (AppiumBy.ACCESSIBILITY_ID, 'Zero'),
        '1': (AppiumBy.ACCESSIBILITY_ID, 'One'),
        '2': (AppiumBy.ACCESSIBILITY_ID, 'Two'),
        '3': (AppiumBy.ACCESSIBILITY_ID, 'Three'),
        '4': (AppiumBy.ACCESSIBILITY_ID, 'Four'),
        '5': (AppiumBy.ACCESSIBILITY_ID, 'Five'),
        '6': (AppiumBy.ACCESSIBILITY_ID, 'Six'),
        '7': (AppiumBy.ACCESSIBILITY_ID, 'Seven'),
        '8': (AppiumBy.ACCESSIBILITY_ID, 'Eight'),
        '9': (AppiumBy.ACCESSIBILITY_ID, 'Nine'),
        # Операции
        'plus': (AppiumBy.ACCESSIBILITY_ID, 'Add'),
        'minus': (AppiumBy.ACCESSIBILITY_ID, 'Subtract'),
        'multiply': (AppiumBy.ACCESSIBILITY_ID, 'Multiply'),
        'divide': (AppiumBy.ACCESSIBILITY_ID, 'Divide'),
        'equals': (AppiumBy.ACCESSIBILITY_ID, 'Equals'),
        'clear': (AppiumBy.ACCESSIBILITY_ID, 'AllClear'),
        'clear_alt': (AppiumBy.ACCESSIBILITY_ID, 'Clear'),  # iOS меняет AC на C после первого ввода
        'delete': (AppiumBy.ACCESSIBILITY_ID, 'Delete'),  # После ввода числа появляется Delete
        # Результат (берем текст из Input view)
        'result': (AppiumBy.XPATH, '//XCUIElementTypeScrollView[@name="StandardInputView"]//XCUIElementTypeStaticText'),
    }
    
    # Локаторы для Android (универсальные, работают с разными калькуляторами)
    # Используют XPATH с текстом для совместимости с Google/Samsung/другими калькуляторами
    ANDROID_LOCATORS = {
        # Цифры (используем content-desc или text)
        '0': (AppiumBy.XPATH, '//*[@content-desc="0" or @text="0"]'),
        '1': (AppiumBy.XPATH, '//*[@content-desc="1" or @text="1"]'),
        '2': (AppiumBy.XPATH, '//*[@content-desc="2" or @text="2"]'),
        '3': (AppiumBy.XPATH, '//*[@content-desc="3" or @text="3"]'),
        '4': (AppiumBy.XPATH, '//*[@content-desc="4" or @text="4"]'),
        '5': (AppiumBy.XPATH, '//*[@content-desc="5" or @text="5"]'),
        '6': (AppiumBy.XPATH, '//*[@content-desc="6" or @text="6"]'),
        '7': (AppiumBy.XPATH, '//*[@content-desc="7" or @text="7"]'),
        '8': (AppiumBy.XPATH, '//*[@content-desc="8" or @text="8"]'),
        '9': (AppiumBy.XPATH, '//*[@content-desc="9" or @text="9"]'),
        # Операции (универсальные паттерны)
        'plus': (AppiumBy.XPATH, '//*[@content-desc="plus" or @content-desc="add" or @content-desc="+" or @text="+"]'),
        'minus': (AppiumBy.XPATH, '//*[@content-desc="minus" or @content-desc="subtract" or @content-desc="−" or @text="−" or @text="-"]'),
        'multiply': (AppiumBy.XPATH, '//*[@content-desc="multiply" or @content-desc="×" or @text="×" or @text="*"]'),
        'divide': (AppiumBy.XPATH, '//*[@content-desc="divide" or @content-desc="÷" or @text="÷" or @text="/"]'),
        'equals': (AppiumBy.XPATH, '//*[@content-desc="equals" or @content-desc="=" or @text="="]'),
        'clear': (AppiumBy.XPATH, '//*[@content-desc="clear" or @content-desc="C" or @content-desc="AC" or @text="C" or @text="AC" or contains(@resource-id, "clear") or contains(@resource-id, "clr")]'),
        # Результат (ищем элемент с числовым текстом в верхней части экрана)
        'result': (AppiumBy.XPATH, '(//*[contains(@resource-id, "result") or contains(@resource-id, "formula") or contains(@resource-id, "display")])[1]'),
    }
    
    def __init__(self):
        """
        Инициализирует Calculator Page Object.
        
        Использует DeviceManager Singleton для доступа к driver.
        """
        self.device_manager = DeviceManager()
        self.driver = self.device_manager.driver
        self.platform = self.device_manager.platform
        self.wait = WebDriverWait(self.driver, 10)
        
        # Выбираем локаторы в зависимости от платформы
        if self.platform == 'ios':
            self.locators = self.IOS_LOCATORS
        elif self.platform == 'android':
            self.locators = self.ANDROID_LOCATORS
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")
        
        logger.info(f"CalculatorPage initialized for platform: {self.platform}")
    
    def _find_element(self, locator_key: str, timeout: int = 10):
        """
        Находит элемент по ключу локатора.
        
        Args:
            locator_key: Ключ локатора из словаря self.locators
            timeout: Время ожидания элемента в секундах
            
        Returns:
            WebElement
            
        Raises:
            TimeoutException: Если элемент не найден
        """
        if locator_key not in self.locators:
            raise ValueError(f"Unknown locator key: {locator_key}")
        
        by, value = self.locators[locator_key]
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            logger.debug(f"Element found: {locator_key}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator_key} (by={by}, value={value})")
            raise
    
    def _tap_element(self, locator_key: str) -> None:
        """
        Нажимает на элемент.
        
        Args:
            locator_key: Ключ локатора элемента
        """
        element = self._find_element(locator_key)
        element.click()
        logger.info(f"Tapped: {locator_key}")
    
    # ==================== Действия с цифрами ====================
    
    def tap_number(self, number: int) -> 'CalculatorPage':
        """
        Нажимает на цифру.
        
        Args:
            number: Цифра от 0 до 9
            
        Returns:
            Self для chain calling
        """
        if not 0 <= number <= 9:
            raise ValueError("Number must be between 0 and 9")
        
        self._tap_element(str(number))
        return self
    
    @allure.step("Enter number: {number}")
    def enter_number(self, number: int) -> 'CalculatorPage':
        """
        Вводит многозначное число (последовательно нажимает цифры).
        
        Args:
            number: Число для ввода (например, 123)
            
        Returns:
            Self для chain calling
        """
        for digit in str(abs(number)):
            self.tap_number(int(digit))
        
        logger.info(f"Entered number: {number}")
        return self
    
    # ==================== Операции ====================
    
    @allure.step("Tap plus button")
    def tap_plus(self) -> 'CalculatorPage':
        """Нажимает кнопку сложения (+)."""
        self._tap_element('plus')
        return self
    
    @allure.step("Tap minus button")
    def tap_minus(self) -> 'CalculatorPage':
        """Нажимает кнопку вычитания (-)."""
        self._tap_element('minus')
        return self
    
    @allure.step("Tap multiply button")
    def tap_multiply(self) -> 'CalculatorPage':
        """Нажимает кнопку умножения (×)."""
        self._tap_element('multiply')
        return self
    
    @allure.step("Tap divide button")
    def tap_divide(self) -> 'CalculatorPage':
        """Нажимает кнопку деления (÷)."""
        self._tap_element('divide')
        return self
    
    @allure.step("Tap equals button")
    def tap_equals(self) -> 'CalculatorPage':
        """Нажимает кнопку равно (=)."""
        self._tap_element('equals')
        return self
    
    @allure.step("Clear display")
    def tap_clear(self) -> 'CalculatorPage':
        """
        Нажимает кнопку очистки (C или AC) или Delete.
        
        В iOS калькуляторе:
        - При запуске показывается "AC" (AllClear)
        - После ввода цифры меняется на "Delete"
        - Метод пытается найти все варианты и использует подходящий
        
        Returns:
            Self для chain calling
        """
        # Пытаемся найти AllClear с коротким таймаутом
        try:
            element = self._find_element('clear', timeout=1)
            element.click()
            logger.info("Clear button tapped (AllClear)")
            return self
        except TimeoutException:
            pass
        
        # Пытаемся найти Clear
        if self.platform == 'ios':
            try:
                element = self._find_element('clear_alt', timeout=1)
                element.click()
                logger.info("Clear button tapped (Clear)")
                return self
            except TimeoutException:
                pass
            
            # Пытаемся найти Delete и нажимаем пока не очистим
            try:
                # Нажимаем Delete многократно, пока результат не станет пустым или "0"
                for _ in range(20):  # Максимум 20 попыток
                    try:
                        result = self.get_result()
                        if not result or result == "0":
                            logger.info("Display cleared using Delete button")
                            return self
                        
                        element = self._find_element('delete', timeout=1)
                        element.click()
                    except:
                        break
                
                logger.info("Display cleared (or mostly cleared)")
                return self
            except TimeoutException as e:
                logger.error(f"Could not find any clear/delete button: {e}")
                raise
        else:
            # Для Android используем стандартную кнопку clear
            try:
                element = self._find_element('clear', timeout=2)
                element.click()
                logger.info("Clear button tapped")
                return self
            except TimeoutException as e:
                logger.error(f"Could not find clear button: {e}")
                raise
    
    # ==================== Получение результата ====================
    
    @allure.step("Get result from display")
    def get_result(self) -> str:
        """
        Получает текущий результат с экрана калькулятора.
        
        Returns:
            Результат как строка (очищенная от невидимых символов и форматирования)
        """
        try:
            result_element = self._find_element('result', timeout=5)
            result_text = result_element.text
            
            # Убираем невидимые Unicode символы (например, U+200E Left-to-Right Mark)
            # которые iOS добавляет к результату
            import re
            cleaned_text = re.sub(r'[\u200e\u200f\u202a-\u202e]', '', result_text)
            
            # Убираем запятые из больших чисел (iOS форматирует 1000 как 1,000)
            cleaned_text = cleaned_text.replace(',', '')
            
            # Для Android: убираем дополнительный текст (Samsung Calculator добавляет "Calculation result")
            if self.platform == 'android':
                # Извлекаем только число из строки типа "4Calculationresult"
                # Ищем паттерн числа в начале строки
                import re
                number_match = re.match(r'^([−\-]?[\d.]+(?:e[+\-]?\d+)?)', cleaned_text)
                if number_match:
                    cleaned_text = number_match.group(1)
                # Убираем любой текстовый мусор в конце
                cleaned_text = re.sub(r'[A-Za-z\s]+$', '', cleaned_text)
            
            logger.info(f"Result: {cleaned_text}")
            return cleaned_text
        except TimeoutException:
            logger.warning("Result element not found, returning empty string")
            return ""
    
    @allure.step("Get result as number")
    def get_result_as_number(self) -> float:
        """
        Получает результат как число (float).
        
        Returns:
            Результат как float
            
        Raises:
            ValueError: Если результат не может быть преобразован в число
        """
        result_text = self.get_result().replace(',', '').replace(' ', '')
        try:
            return float(result_text)
        except ValueError:
            logger.error(f"Cannot convert result to number: {result_text}")
            raise
    
    # ==================== Высокоуровневые методы ====================
    
    @allure.step("Calculate addition: {num1} + {num2}")
    def calculate_addition(self, num1: int, num2: int) -> str:
        """
        Выполняет сложение двух чисел: num1 + num2
        
        Args:
            num1: Первое число
            num2: Второе число
            
        Returns:
            Результат операции как строка
        """
        logger.info(f"Calculating: {num1} + {num2}")
        self.tap_clear()  # Очищаем перед началом
        self.enter_number(num1)
        self.tap_plus()
        self.enter_number(num2)
        self.tap_equals()
        return self.get_result()
    
    @allure.step("Calculate subtraction: {num1} - {num2}")
    def calculate_subtraction(self, num1: int, num2: int) -> str:
        """
        Выполняет вычитание: num1 - num2
        
        Args:
            num1: Первое число
            num2: Второе число
            
        Returns:
            Результат операции как строка
        """
        logger.info(f"Calculating: {num1} - {num2}")
        self.tap_clear()
        self.enter_number(num1)
        self.tap_minus()
        self.enter_number(num2)
        self.tap_equals()
        return self.get_result()
    
    @allure.step("Calculate multiplication: {num1} × {num2}")
    def calculate_multiplication(self, num1: int, num2: int) -> str:
        """
        Выполняет умножение: num1 × num2
        
        Args:
            num1: Первое число
            num2: Второе число
            
        Returns:
            Результат операции как строка
        """
        logger.info(f"Calculating: {num1} × {num2}")
        self.tap_clear()
        self.enter_number(num1)
        self.tap_multiply()
        self.enter_number(num2)
        self.tap_equals()
        return self.get_result()
    
    @allure.step("Calculate division: {num1} ÷ {num2}")
    def calculate_division(self, num1: int, num2: int) -> str:
        """
        Выполняет деление: num1 ÷ num2
        
        Args:
            num1: Первое число (делимое)
            num2: Второе число (делитель)
            
        Returns:
            Результат операции как строка
        """
        logger.info(f"Calculating: {num1} ÷ {num2}")
        self.tap_clear()
        self.enter_number(num1)
        self.tap_divide()
        self.enter_number(num2)
        self.tap_equals()
        return self.get_result()
    
    @allure.step("Clear calculator display")
    def clear_display(self) -> 'CalculatorPage':
        """
        Очищает дисплей калькулятора.
        
        Returns:
            Self для chain calling
        """
        self.tap_clear()
        logger.info("Display cleared")
        return self
    
    @allure.step("Check if calculator is opened")
    def is_calculator_opened(self) -> bool:
        """
        Проверяет, открыт ли калькулятор (проверяет наличие кнопки 0).
        
        Returns:
            True если калькулятор открыт, False иначе
        """
        try:
            self._find_element('0', timeout=3)
            return True
        except TimeoutException:
            return False

