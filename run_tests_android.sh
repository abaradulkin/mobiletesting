#!/bin/bash
# Скрипт для запуска тестов на Android устройстве

set -e  # Остановка при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}🤖 Mobile Testing - Android${NC}"
echo -e "${BLUE}================================${NC}"

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Виртуальное окружение не найдено${NC}"
    echo -e "${YELLOW}💡 Создайте его: python3 -m venv venv${NC}"
    exit 1
fi

# Активация виртуального окружения
echo -e "${BLUE}📦 Активация виртуального окружения...${NC}"
source venv/bin/activate

# Проверка adb
echo -e "${BLUE}🔍 Проверка adb...${NC}"
if ! command -v adb &> /dev/null; then
    echo -e "${RED}❌ adb не найден${NC}"
    echo -e "${YELLOW}💡 Установите Android SDK и добавьте platform-tools в PATH${NC}"
    exit 1
fi

# Проверка устройств
echo -e "${BLUE}📱 Проверка подключенных устройств...${NC}"
DEVICES=$(adb devices | grep -w "device" | wc -l)
if [ "$DEVICES" -eq 0 ]; then
    echo -e "${RED}❌ Нет подключенных Android устройств${NC}"
    echo -e "${YELLOW}💡 Подключите устройство или запустите эмулятор${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Найдено устройств: $DEVICES${NC}"

# Проверка Appium сервера
echo -e "${BLUE}🔌 Проверка Appium сервера...${NC}"
if ! curl -s http://localhost:4723/status > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Appium сервер не запущен${NC}"
    echo -e "${BLUE}🚀 Запуск Appium сервера в фоне...${NC}"
    appium > /dev/null 2>&1 &
    APPIUM_PID=$!
    echo -e "${GREEN}✅ Appium запущен (PID: $APPIUM_PID)${NC}"
    sleep 3
else
    echo -e "${GREEN}✅ Appium сервер работает${NC}"
    APPIUM_PID=""
fi

# Определение типа запуска
TEST_TYPE=${1:-all}
case "$TEST_TYPE" in
    smoke)
        echo -e "${BLUE}🚬 Запуск SMOKE тестов на Android${NC}"
        PYTEST_ARGS="-m smoke --platform android"
        ;;
    regression)
        echo -e "${BLUE}🔄 Запуск REGRESSION тестов на Android${NC}"
        PYTEST_ARGS="-m regression --platform android"
        ;;
    android_only)
        echo -e "${BLUE}🤖 Запуск Android-специфичных тестов${NC}"
        PYTEST_ARGS="-m android_only --platform android"
        ;;
    allure)
        echo -e "${BLUE}📊 Запуск тестов с Allure отчетами${NC}"
        PYTEST_ARGS="--platform android --alluredir=allure-results"
        ;;
    *)
        echo -e "${BLUE}🧪 Запуск ВСЕХ тестов на Android${NC}"
        PYTEST_ARGS="--platform android"
        ;;
esac

# Запуск тестов
echo -e "${BLUE}================================${NC}"
pytest $PYTEST_ARGS -v

# Сохранение кода возврата
TEST_EXIT_CODE=$?

# Остановка Appium если запускали
if [ -n "$APPIUM_PID" ]; then
    echo -e "${BLUE}🛑 Остановка Appium сервера...${NC}"
    kill $APPIUM_PID 2>/dev/null || true
fi

# Итоги
echo -e "${BLUE}================================${NC}"
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Тесты прошли успешно!${NC}"
else
    echo -e "${RED}❌ Тесты завершились с ошибками${NC}"
fi
echo -e "${BLUE}================================${NC}"

exit $TEST_EXIT_CODE

