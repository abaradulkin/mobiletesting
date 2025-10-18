# 🤖 Настройка Android для Mobile Testing

Подробное руководство по настройке Android окружения для запуска автоматизированных тестов.

---

## 📋 Содержание

1. [Установка Android SDK](#установка-android-sdk)
2. [Настройка переменных окружения](#настройка-переменных-окружения)
3. [Установка Appium](#установка-appium)
4. [Настройка эмулятора](#настройка-эмулятора)
5. [Настройка физического устройства](#настройка-физического-устройства)
6. [Установка Google Calculator](#установка-google-calculator)
7. [Проверка настройки](#проверка-настройки)
8. [Запуск тестов](#запуск-тестов)
9. [Troubleshooting](#troubleshooting)

---

## 🛠️ Установка Android SDK

### macOS

**Вариант 1: Android Studio (рекомендуется)**

1. Скачайте [Android Studio](https://developer.android.com/studio)
2. Установите и запустите Android Studio
3. Откройте **Settings → Appearance & Behavior → System Settings → Android SDK**
4. Установите:
   - ✅ Android SDK Platform (последняя версия)
   - ✅ Android SDK Command-line Tools
   - ✅ Android SDK Platform-Tools
   - ✅ Android SDK Build-Tools

**Вариант 2: Homebrew (только command-line tools)**

```bash
brew install --cask android-platform-tools
brew install --cask android-commandlinetools
```

### Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install android-sdk

# Или скачайте напрямую
wget https://dl.google.com/android/repository/commandlinetools-linux-latest.zip
unzip commandlinetools-linux-latest.zip -d ~/Android/cmdline-tools
```

### Windows

1. Скачайте [Android Studio](https://developer.android.com/studio)
2. Установите через инсталлятор
3. Следуйте мастеру настройки

---

## 🔧 Настройка переменных окружения

### macOS/Linux

Добавьте в `~/.zshrc` (macOS) или `~/.bashrc` (Linux):

```bash
# Android SDK
export ANDROID_HOME=$HOME/Library/Android/sdk  # macOS
# export ANDROID_HOME=$HOME/Android/Sdk        # Linux

export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/tools/bin
```

Применить изменения:
```bash
source ~/.zshrc  # или ~/.bashrc
```

### Windows

1. Откройте **System Properties → Advanced → Environment Variables**
2. Создайте новую системную переменную:
   - **Переменная:** `ANDROID_HOME`
   - **Значение:** `C:\Users\YOUR_USERNAME\AppData\Local\Android\Sdk`
3. Добавьте в PATH:
   - `%ANDROID_HOME%\platform-tools`
   - `%ANDROID_HOME%\emulator`
   - `%ANDROID_HOME%\cmdline-tools\latest\bin`

---

## 📱 Установка Appium

### Установка Node.js

**macOS:**
```bash
brew install node
```

**Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Windows:**
Скачайте инсталлятор с [nodejs.org](https://nodejs.org/)

### Установка Appium

```bash
npm install -g appium

# Установка драйвера UiAutomator2 для Android
appium driver install uiautomator2
```

### Проверка установки

```bash
appium --version
appium driver list
```

---

## 🖥️ Настройка эмулятора

### Через Android Studio

1. Откройте **Android Studio**
2. **Tools → Device Manager** (или **AVD Manager**)
3. Нажмите **Create Device**
4. Выберите устройство (например, Pixel 6)
5. Выберите системный образ:
   - Рекомендуется: **Android 13 (API 33)** или выше
   - Скачайте образ, если не установлен
6. Настройте параметры:
   - **RAM:** минимум 2GB
   - **VM Heap:** 512MB
   - Включите **Hardware Acceleration** (HAXM/KVM)
7. Нажмите **Finish**

### Запуск эмулятора

**Через Android Studio:**
- Device Manager → ▶️ Play

**Через командную строку:**
```bash
# Список доступных эмуляторов
emulator -list-avds

# Запуск конкретного эмулятора
emulator -avd Pixel_6_API_33
```

---

## 📲 Настройка физического устройства

### 1. Включить Developer Options

На устройстве:
1. **Settings → About Phone**
2. Нажмите на **Build Number** 7 раз
3. Введите PIN/пароль
4. Появится сообщение "You are now a developer!"

### 2. Включить USB Debugging

1. **Settings → System → Developer Options**
2. Включите **USB Debugging**
3. Включите **Install via USB** (опционально)

### 3. Подключить к компьютеру

1. Подключите устройство через USB
2. На устройстве появится запрос "Allow USB Debugging?" → **Allow**
3. Можете отметить "Always allow from this computer"

### 4. Проверка подключения

```bash
adb devices
```

Вы должны увидеть:
```
List of devices attached
XXXXXXXXXXXXXX	device
```

Если видите `unauthorized` - разрешите на устройстве.

---

## 🧮 Установка Google Calculator

### Вариант 1: Google Play Store

1. Откройте **Google Play Store** на устройстве/эмуляторе
2. Найдите **"Google Calculator"** или **"Calculator"**
3. Установите

### Вариант 2: ADB (если Play Store недоступен)

```bash
# Скачайте APK с apkmirror.com или другого источника
# Установите через adb
adb install calculator.apk
```

### Проверка установки

```bash
adb shell pm list packages | grep calculator
```

Должно показать:
```
package:com.google.android.calculator
```

---

## ✅ Проверка настройки

Используйте наш скрипт проверки:

```bash
python3 debug_android.py
```

Скрипт проверит:
- ✅ Наличие adb
- ✅ Подключенные устройства
- ✅ Установку Google Calculator
- ✅ Доступность Appium сервера
- ✅ Конфигурационный файл

Если всё ✅ - можно запускать тесты!

---

## 🚀 Запуск тестов

### Запуск Appium сервера

```bash
appium
```

Должно показать:
```
[Appium] Welcome to Appium v2.x.x
[Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

### Запуск тестов

**Smoke тесты:**
```bash
./run_tests_android.sh smoke
```

**Все тесты:**
```bash
./run_tests_android.sh
```

**С Allure отчетами:**
```bash
./run_tests_android.sh allure
```

**Вручную через pytest:**
```bash
source venv/bin/activate
pytest --platform android -m smoke -v
```

---

## 🔧 Troubleshooting

### Проблема: `adb: command not found`

**Решение:**
```bash
# Проверьте ANDROID_HOME
echo $ANDROID_HOME

# Если пустой - добавьте в ~/.zshrc:
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
source ~/.zshrc
```

---

### Проблема: `adb devices` показывает `unauthorized`

**Решение:**
1. На устройстве появится запрос USB Debugging - нажмите **Allow**
2. Если запрос не появился:
```bash
adb kill-server
adb start-server
adb devices
```

---

### Проблема: `Could not find a connected device`

**Решение:**
```bash
# Проверьте список устройств
adb devices

# Если пусто:
# 1. Перезапустите adb сервер
adb kill-server && adb start-server

# 2. Перезапустите эмулятор
emulator -avd YOUR_AVD_NAME

# 3. Переподключите физическое устройство
```

---

### Проблема: `An unknown server-side error occurred`

**Решение:**
1. Проверьте, что Google Calculator установлен:
```bash
adb shell pm list packages | grep calculator
```

2. Проверьте правильность appPackage и appActivity в `config/android.json`:
```json
{
  "appPackage": "com.google.android.calculator",
  "appActivity": "com.android.calculator2.Calculator"
}
```

3. Попробуйте запустить Calculator вручную:
```bash
adb shell am start -n com.google.android.calculator/com.android.calculator2.Calculator
```

---

### Проблема: Медленная работа эмулятора

**Решение:**
1. Включите аппаратное ускорение (HAXM для Intel, KVM для Linux)
2. Увеличьте RAM для AVD (минимум 2GB)
3. Используйте системный образ x86/x86_64 вместо ARM
4. Закройте лишние приложения на компьютере

---

### Проблема: `Element not found` в тестах

**Решение:**
1. Возможно изменились локаторы в новой версии Calculator
2. Используйте **Appium Inspector** для проверки:
```bash
npm install -g appium-inspector
appium-inspector
```

3. Подключитесь к устройству и проверьте актуальные локаторы

---

## 📚 Полезные команды ADB

```bash
# Список устройств
adb devices

# Список установленных пакетов
adb shell pm list packages

# Установка APK
adb install app.apk

# Удаление приложения
adb uninstall com.google.android.calculator

# Запуск приложения
adb shell am start -n com.google.android.calculator/com.android.calculator2.Calculator

# Просмотр логов
adb logcat

# Скриншот
adb shell screencap /sdcard/screen.png
adb pull /sdcard/screen.png

# Перезапуск adb
adb kill-server && adb start-server
```

---

## 🎯 Следующие шаги

После успешной настройки Android:

1. ✅ Запустите smoke тесты: `./run_tests_android.sh smoke`
2. ✅ Запустите полный набор тестов
3. ✅ Сравните результаты с iOS тестами
4. ✅ Настройте CI/CD для автоматического запуска

---

## 📞 Поддержка

Если проблема не решена:
1. Проверьте `test_execution.log`
2. Посмотрите логи Appium
3. Используйте `debug_android.py` для диагностики
4. Создайте issue в репозитории с подробным описанием

---

**Удачных тестов! 🚀**

