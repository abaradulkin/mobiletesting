# 🚀 Быстрый старт за 5 минут

## Шаг 1: Установка зависимостей

```bash
# Создайте и активируйте виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt
```

## Шаг 2: Установка Appium (если еще не установлен)

```bash
# Установите Appium глобально
npm install -g appium

# Установите драйверы
appium driver install xcuitest      # Для iOS
appium driver install uiautomator2  # Для Android
```

## Шаг 3: Запуск Appium сервера

Откройте новый терминал и запустите:

```bash
appium
```

Вы должны увидеть:
```
[Appium] Welcome to Appium v2.x.x
[Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

## Шаг 4: Подготовка устройства

### Для iOS:
```bash
# Запустите iOS Simulator
open -a Simulator

# Или откройте через Xcode -> Open Developer Tool -> Simulator

# Проверьте доступные устройства
xcrun simctl list devices
```

### Для Android:
```bash
# Запустите Android эмулятор
emulator -avd <AVD_NAME>

# Или создайте новый через Android Studio -> AVD Manager

# Проверьте подключенные устройства
adb devices
```

## Шаг 5: Запуск тестов

```bash
# Запуск на iOS (по умолчанию)
pytest

# Запуск на Android
pytest --platform android

# Запуск только smoke тестов
pytest -m smoke

# Запуск с HTML отчетом
pytest --html=report.html --self-contained-html
```

### Или используйте скрипт:

```bash
# iOS
./run_tests.sh ios

# Android
./run_tests.sh android

# iOS smoke tests
./run_tests.sh ios smoke
```

## 🎉 Готово!

Если все прошло успешно, вы должны увидеть:

```
tests/test_example.py::TestCalculatorBasic::test_addition_2_plus_3 PASSED
tests/test_example.py::TestCalculatorBasic::test_addition_using_high_level_method PASSED
...

====== X passed in Y.YY seconds ======
```

## 🐛 Возможные проблемы

### Appium сервер не запускается
```bash
# Проверьте установку
appium --version

# Переустановите если нужно
npm uninstall -g appium
npm install -g appium
```

### iOS Simulator не открывается
```bash
# Сбросьте симулятор
xcrun simctl erase all

# Откройте через Xcode
xcode-select --install
```

### Android эмулятор не запускается
```bash
# Проверьте список AVD
emulator -list-avds

# Создайте новый через Android Studio
# Tools -> AVD Manager -> Create Virtual Device
```

### Тест не может найти элементы
```bash
# Получите page source для отладки
pytest tests/test_example.py -k "test_addition" -s

# В тесте добавьте:
# print(app.get_page_source())
```

## 📚 Следующие шаги

1. Изучите `README.md` для подробной документации
2. Посмотрите `tests/test_example.py` для примеров тестов
3. Изучите `page_objects/calculator_page.py` для Page Object Pattern
4. Настройте `config/*.json` под свои устройства

## 💡 Полезные команды

```bash
# Запуск конкретного теста
pytest tests/test_example.py::TestCalculatorBasic::test_addition_2_plus_3

# Запуск с подробным выводом
pytest -vv

# Запуск с выводом print statements
pytest -s

# Перезапуск упавших тестов
pytest --reruns 2

# Параллельный запуск
pytest -n 2

# Остановка на первом падении
pytest -x
```

## 🎓 Структура проекта

```
mobiletesting/
├── config/              # Настройки для разных платформ
├── utils/               # DeviceManager и утилиты
├── page_objects/        # Page Objects для UI
├── tests/               # Ваши тесты
├── conftest.py          # Pytest fixtures
└── pytest.ini           # Pytest конфигурация
```

---

**Нужна помощь?** Откройте issue в репозитории или обратитесь к документации:
- [Appium Docs](http://appium.io/docs/)
- [Pytest Docs](https://docs.pytest.org/)

