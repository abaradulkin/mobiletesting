# Mobile Testing Framework - iOS/Android/Windows

Фреймворк для автоматизации тестирования мобильных приложений с использованием Python, Pytest и Appium.

## 🏗️ Архитектура проекта

```
mobiletesting/
├── config/                    # Конфигурационные файлы
│   ├── ios.json              # Capabilities для iOS
│   ├── android.json          # Capabilities для Android
│   └── windows.json          # Capabilities для Windows
├── utils/                     # Утилиты
│   └── device_manager.py     # Singleton для управления Appium сессией
├── page_objects/              # Page Objects
│   └── calculator_page.py    # Page Object для калькулятора
├── tests/                     # Тесты
│   └── test_example.py       # Примеры тестов
├── docs/                      # Документация
│   └── test_automation_strategy.md
├── conftest.py               # Pytest fixtures и hooks
├── pytest.ini                # Pytest конфигурация
└── requirements.txt          # Python зависимости
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Установка Appium

```bash
# Установите Node.js (если еще не установлен)
# Затем установите Appium
npm install -g appium

# Установите драйверы
appium driver install xcuitest   # Для iOS
appium driver install uiautomator2  # Для Android
appium driver install windows    # Для Windows (опционально)
```

### 3. Запуск Appium сервера

```bash
# Запустите Appium на порту 4723 (по умолчанию)
appium

# Или с явным указанием порта
appium --port 4723
```

### 4. Настройка устройств

#### iOS:
1. Подключите iPhone или запустите iOS Simulator
2. Убедитесь, что установлен Xcode и WebDriverAgent
3. Проверьте UDID устройства: `xcrun xctrace list devices`
4. Обновите `config/ios.json` если нужно

#### Android:
1. Установите Android SDK и настройте `ANDROID_HOME`
2. Подключите Android устройство или запустите эмулятор
3. Включите Developer Options и USB Debugging
4. Проверьте устройство: `adb devices`
5. Установите Google Calculator на устройство
6. Обновите `config/android.json` если нужно

**📖 Подробная инструкция:** [docs/ANDROID_SETUP.md](docs/ANDROID_SETUP.md)

**🔍 Быстрая проверка настройки Android:**
```bash
python3 debug_android.py
```

**🚀 Быстрый запуск тестов на Android:**
```bash
./run_tests_android.sh smoke     # Smoke тесты
./run_tests_android.sh           # Все тесты
./run_tests_android.sh allure    # С Allure отчетами
```

### 5. Запуск тестов

```bash
# Запуск всех тестов на iOS (по умолчанию)
pytest

# Запуск тестов на Android
pytest --platform android

# Или используйте удобный скрипт для Android
./run_tests_android.sh smoke      # Smoke тесты
./run_tests_android.sh            # Все тесты

# Запуск тестов на Windows
pytest --platform windows

# Запуск конкретного теста
pytest tests/test_example.py::TestCalculatorBasic::test_addition_2_plus_3

# Запуск только smoke тестов
pytest -m smoke

# Запуск с HTML отчетом
pytest --html=report.html --self-contained-html

# Параллельный запуск (требует pytest-xdist)
pytest -n 2  # Запуск на 2 параллельных workers
```

### 6. Allure отчеты

Проект поддерживает генерацию красивых и детальных отчетов с помощью Allure Framework.

#### Установка Allure CLI

**macOS:**
```bash
brew install allure
```

**Windows:**
```bash
scoop install allure
```

**Linux:**
```bash
# Скачайте и распакуйте из https://github.com/allure-framework/allure2/releases
```

#### Запуск тестов с Allure

```bash
# Запуск тестов с сохранением результатов для Allure
pytest --alluredir=allure-results

# Запуск только smoke тестов с Allure
pytest -m smoke --alluredir=allure-results

# Запуск тестов на Android с Allure
pytest --platform android --alluredir=allure-results
```

#### Генерация и просмотр отчета

```bash
# Генерация отчета
allure generate allure-results -o allure-report --clean

# Открытие отчета в браузере
allure open allure-report

# Или генерация и открытие одной командой
allure serve allure-results
```

#### Что включено в Allure отчеты

- ✅ **Группировка по фичам**: Addition, Subtraction
- ✅ **Детальные шаги**: Каждое действие (enter number, tap button) отображается как отдельный шаг
- ✅ **Скриншоты при падении**: Автоматически прикрепляются к отчету
- ✅ **Severity levels**: Critical (smoke тесты), Normal (остальные)
- ✅ **Parametrized tests**: Четко показывает все комбинации параметров
- ✅ **История запусков**: Тренды и статистика по времени
- ✅ **Categorization**: Автоматическая категоризация ошибок

## 📱 DeviceManager - Центральный компонент

`DeviceManager` - это Singleton класс, который обеспечивает:
- Единую точку доступа к Appium driver из любой части кода
- Управление жизненным циклом приложения
- Управление устройством (ориентация, сеть, и т.д.)

### Пример использования:

```python
from utils.device_manager import DeviceManager

# В тестах DeviceManager уже инициализирован через fixture
def test_example(app):
    # app - это DeviceManager instance
    
    # Доступ к driver
    driver = app.driver
    
    # Управление приложением
    app.restart_app()
    app.stop_app()
    app.start_app()
    
    # Проверка состояния
    is_running = app.is_app_running()
    
    # Управление устройством
    app.rotate_to_landscape()
    app.rotate_to_portrait()
    app.background_app(5)  # В фон на 5 секунд
    
    # Android specific
    app.toggle_wifi(enable=False)
    app.toggle_airplane_mode(enable=True)
    
    # Утилиты
    app.take_screenshot("screenshot.png")
    page_source = app.get_page_source()
```

### Использование в Page Objects:

```python
from utils.device_manager import DeviceManager

class MyPage:
    def __init__(self):
        # Получаем DeviceManager Singleton
        self.device_manager = DeviceManager()
        self.driver = self.device_manager.driver
        
    def some_action(self):
        # Используем driver
        element = self.driver.find_element(...)
```

## 📄 Page Object Pattern

Все взаимодействия с UI должны быть инкапсулированы в Page Objects.

### Пример Page Object:

```python
from utils.device_manager import DeviceManager
from appium.webdriver.common.appiumby import AppiumBy

class CalculatorPage:
    def __init__(self):
        self.device_manager = DeviceManager()
        self.driver = self.device_manager.driver
    
    def tap_number(self, number: int):
        locator = (AppiumBy.ACCESSIBILITY_ID, str(number))
        element = self.driver.find_element(*locator)
        element.click()
        return self  # Для chain calling
    
    def calculate_addition(self, num1: int, num2: int) -> str:
        self.enter_number(num1)
        self.tap_plus()
        self.enter_number(num2)
        self.tap_equals()
        return self.get_result()
```

## 🧪 Написание тестов

### Базовая структура теста:

```python
import pytest
from page_objects.calculator_page import CalculatorPage

class TestCalculator:
    @pytest.fixture(autouse=True)
    def setup(self, app):
        """Setup перед каждым тестом"""
        self.app = app
        self.calculator = CalculatorPage()
    
    def test_addition(self):
        """Тест сложения"""
        # Act
        result = self.calculator.calculate_addition(2, 3)
        
        # Assert
        assert result == "5"
```

### Использование маркеров:

```python
@pytest.mark.smoke
def test_critical_feature():
    """Smoke тест"""
    pass

@pytest.mark.regression
def test_detailed_feature():
    """Regression тест"""
    pass

@pytest.mark.ios
def test_ios_specific():
    """Тест только для iOS"""
    pass

@pytest.mark.parametrize("num1,num2,expected", [
    (1, 1, "2"),
    (5, 5, "10"),
])
def test_parametrized(num1, num2, expected):
    """Параметризованный тест"""
    pass
```

## ⚙️ Конфигурация

### Capabilities (config/*.json)

Capabilities можно настраивать для каждой платформы в соответствующих JSON файлах:

- `config/ios.json` - настройки для iOS
- `config/android.json` - настройки для Android
- `config/windows.json` - настройки для Windows

### Командная строка

```bash
# Платформа (по умолчанию ios)
pytest --platform android

# Appium server URL (по умолчанию http://localhost:4723)
pytest --appium-server http://192.168.1.100:4723

# Комбинированные опции
pytest --platform android --appium-server http://remote-server:4723 -v
```

## 📊 Отчетность

### HTML отчеты:

```bash
pytest --html=report.html --self-contained-html
```

### Allure отчеты:

```bash
# Запуск тестов с генерацией Allure результатов
pytest --alluredir=allure-results

# Просмотр отчета
allure serve allure-results
```

## 🐛 Отладка

### Скриншоты при падении

Скриншоты автоматически создаются при падении тестов и сохраняются в папку `screenshots/`.

### Логи

Логи сохраняются в `test_execution.log` с детальной информацией о выполнении тестов.

### Page Source

Можно получить XML page source для анализа:

```python
def test_debug(app):
    page_source = app.get_page_source()
    print(page_source)  # Или сохраните в файл
```

## 🔧 Продвинутое использование

### Параллельный запуск тестов:

```bash
# Запуск на 4 параллельных workers
pytest -n 4

# Автоматическое определение количества CPU
pytest -n auto
```

### Перезапуск упавших тестов:

```bash
# Перезапустить упавшие тесты 2 раза
pytest --reruns 2

# С задержкой между перезапусками
pytest --reruns 2 --reruns-delay 5
```

## 📝 Best Practices

1. **Используйте Page Object Pattern** - вся логика UI в Page Objects
2. **Singleton для DeviceManager** - единая точка доступа к driver
3. **Изоляция тестов** - каждый тест должен быть независимым
4. **Явные ожидания** - используйте WebDriverWait вместо time.sleep()
5. **Осмысленные имена** - тесты и методы должны быть понятными
6. **Маркеры** - организуйте тесты по категориям (smoke, regression, и т.д.)
7. **Логирование** - используйте логирование для отладки
8. **Скриншоты** - делайте скриншоты при падении тестов

## 🤝 Вклад в проект

1. Создайте feature branch
2. Добавьте тесты для новой функциональности
3. Убедитесь, что все тесты проходят
4. Создайте Pull Request

## 📚 Дополнительные ресурсы

- [Appium Documentation](http://appium.io/docs/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Selenium Python Bindings](https://selenium-python.readthedocs.io/)

## 📄 Лицензия

MIT License

---

**Версия**: 1.0  
**Дата создания**: Октябрь 2025

