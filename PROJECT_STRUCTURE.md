# 📁 Структура проекта Mobile Testing Framework

## Полная структура

```
mobiletesting/
│
├── 📁 config/                          # Конфигурационные файлы
│   ├── ios.json                        # Appium capabilities для iOS
│   ├── android.json                    # Appium capabilities для Android
│   └── windows.json                    # Appium capabilities для Windows
│
├── 📁 utils/                           # Утилиты и вспомогательные классы
│   ├── __init__.py                     # Package init
│   └── device_manager.py               # ⭐ DeviceManager Singleton класс
│
├── 📁 page_objects/                    # Page Object Pattern
│   ├── __init__.py                     # Package init
│   └── calculator_page.py              # Page Object для калькулятора
│
├── 📁 tests/                           # Тесты
│   ├── __init__.py                     # Package init
│   └── test_example.py                 # 🧪 Примеры тестов калькулятора
│
├── 📁 docs/                            # Документация
│   ├── test_automation_strategy.md     # Стратегия автоматизации (GTA Online архитектура)
│   └── ...                             # Другие документы
│
├── conftest.py                         # ⚙️ Pytest fixtures и hooks
├── pytest.ini                          # ⚙️ Pytest конфигурация
├── requirements.txt                    # 📦 Python зависимости
├── .gitignore                          # Git ignore файл
│
├── README.md                           # 📖 Основная документация
├── QUICKSTART.md                       # 🚀 Быстрый старт за 5 минут
├── PROJECT_STRUCTURE.md                # 📁 Этот файл
└── run_tests.sh                        # 🔧 Скрипт для запуска тестов
```

## Описание компонентов

### 🎯 Ключевые файлы

#### 1. `utils/device_manager.py`
**Singleton класс для управления Appium сессией**

- ✅ Единственный экземпляр для всего фреймворка
- ✅ Управление жизненным циклом приложения (start/stop/restart)
- ✅ Управление устройством (ориентация, сеть)
- ✅ Доступ к Appium driver из любой точки кода
- ✅ Кросс-платформенная поддержка (iOS, Android, Windows)

**Основные методы:**
```python
# Управление приложением
start_app()
stop_app()
restart_app()
is_app_running()
background_app(seconds)

# Управление устройством
rotate_to_landscape()
rotate_to_portrait()
toggle_wifi(enable)
toggle_airplane_mode(enable)

# Утилиты
take_screenshot(filename)
get_page_source()
```

#### 2. `conftest.py`
**Pytest конфигурация и fixtures**

- ✅ Фикстура `device_manager` - инициализация Appium сессии
- ✅ Фикстура `app` - доступ к DeviceManager в тестах
- ✅ Фикстура `screenshot_on_failure` - автоматические скриншоты
- ✅ Hook `pytest_addoption` - опция `--platform`
- ✅ Загрузка capabilities из JSON файлов

**Использование:**
```python
def test_example(app):
    # app - это DeviceManager instance
    driver = app.driver
    app.rotate_to_landscape()
```

#### 3. `page_objects/calculator_page.py`
**Page Object для калькулятора**

- ✅ Инкапсуляция локаторов для iOS и Android
- ✅ Методы для взаимодействия с UI
- ✅ Высокоуровневые методы (calculate_addition, etc.)
- ✅ Chain calling поддержка
- ✅ Автоматический выбор локаторов по платформе

**Пример:**
```python
calculator = CalculatorPage()
result = calculator.calculate_addition(2, 3)
assert result == "5"
```

#### 4. `tests/test_example.py`
**Примеры тестов**

- ✅ `TestCalculatorBasic` - базовые математические операции
- ✅ `TestCalculatorSmoke` - smoke тесты
- ✅ `TestCalculatorEdgeCases` - граничные случаи
- ✅ `TestDeviceManagerFeatures` - демонстрация DeviceManager
- ✅ Параметризованные тесты
- ✅ Использование маркеров

### ⚙️ Конфигурационные файлы

#### `config/ios.json`
```json
{
  "platformName": "iOS",
  "platformVersion": "17.0",
  "deviceName": "iPhone 15",
  "automationName": "XCUITest",
  "bundleId": "com.apple.calculator"
}
```

#### `config/android.json`
```json
{
  "platformName": "Android",
  "platformVersion": "13.0",
  "deviceName": "Android Emulator",
  "automationName": "UiAutomator2",
  "appPackage": "com.google.android.calculator",
  "appActivity": "com.android.calculator2.Calculator"
}
```

### 📦 Зависимости (requirements.txt)

- `Appium-Python-Client` - Appium клиент
- `selenium` - WebDriver
- `pytest` - Тестовый фреймворк
- `pytest-html` - HTML отчеты
- `pytest-xdist` - Параллельный запуск
- `pytest-timeout` - Таймауты
- `pytest-rerunfailures` - Перезапуск упавших тестов
- `allure-pytest` - Allure отчеты

## 🔄 Поток работы

### 1. Инициализация (conftest.py)

```
pytest запуск
    ↓
pytest_addoption() - добавляет --platform опцию
    ↓
device_manager fixture
    ↓
load_capabilities() - загружает JSON конфиг
    ↓
create_driver() - создает Appium driver
    ↓
DeviceManager.initialize_driver() - инициализирует Singleton
    ↓
start_app() - запускает приложение
    ↓
yield DeviceManager - передает в тесты
```

### 2. Выполнение теста

```
test_example(app)
    ↓
CalculatorPage() - создает Page Object
    ↓
DeviceManager() - получает Singleton instance
    ↓
calculator.calculate_addition(2, 3)
    ↓
Взаимодействие с UI через driver
    ↓
Проверка результата
```

### 3. Cleanup

```
Все тесты завершены
    ↓
device_manager fixture teardown
    ↓
DeviceManager.close_app()
    ↓
driver.quit()
    ↓
DeviceManager.reset_instance()
```

## 🎨 Паттерны и практики

### Singleton Pattern
```python
class DeviceManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Page Object Pattern
```python
class CalculatorPage:
    def __init__(self):
        self.device_manager = DeviceManager()
        self.driver = self.device_manager.driver
    
    def tap_number(self, number):
        # Инкапсуляция взаимодействия с UI
        pass
```

### Fixture Pattern
```python
@pytest.fixture(scope="session")
def device_manager(platform, appium_server_url):
    # Setup
    dm = DeviceManager()
    # ...
    yield dm
    # Teardown
    dm.close_app()
```

### Chain Calling
```python
self.calculator\
    .clear_display()\
    .enter_number(2)\
    .tap_plus()\
    .enter_number(3)\
    .tap_equals()
```

## 🚀 Команды запуска

```bash
# Базовый запуск
pytest

# С указанием платформы
pytest --platform android

# С маркерами
pytest -m smoke

# Конкретный тест
pytest tests/test_example.py::TestCalculatorBasic::test_addition_2_plus_3

# С HTML отчетом
pytest --html=report.html --self-contained-html

# Параллельно
pytest -n 4

# С перезапуском
pytest --reruns 2

# Через скрипт
./run_tests.sh ios
./run_tests.sh android smoke
```

## 📊 Генерация отчетов

### HTML
```bash
pytest --html=report.html --self-contained-html
# Результат: report.html
```

### Allure
```bash
pytest --alluredir=allure-results
allure serve allure-results
# Результат: интерактивный отчет в браузере
```

### Логи
- `test_execution.log` - детальные логи
- `screenshots/` - скриншоты при падении тестов

## 🔧 Расширение фреймворка

### Добавление нового Page Object
1. Создайте файл в `page_objects/`
2. Наследуйтесь от базового класса или используйте DeviceManager
3. Добавьте локаторы для всех платформ
4. Реализуйте методы взаимодействия
5. Добавьте в `page_objects/__init__.py`

### Добавление новой платформы
1. Создайте `config/{platform}.json`
2. Добавьте capabilities
3. Обновите `conftest.py` если нужна специальная логика
4. Добавьте локаторы в Page Objects

### Добавление утилит
1. Создайте файл в `utils/`
2. Реализуйте функциональность
3. Добавьте в `utils/__init__.py`
4. Используйте в тестах или Page Objects

## 📚 Дополнительные ресурсы

- **README.md** - полная документация
- **QUICKSTART.md** - быстрый старт
- **docs/test_automation_strategy.md** - общая стратегия

---

**Создано**: Октябрь 2025  
**Версия**: 1.0  
**Архитектура**: Singleton + Page Object Pattern + Pytest Fixtures

