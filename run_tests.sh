#!/bin/bash
# Скрипт для быстрого запуска тестов

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Mobile Testing Framework${NC}"
echo ""

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Проверка Appium
if ! command -v appium &> /dev/null; then
    echo -e "${RED}❌ Appium not installed!${NC}"
    echo "Install Appium: npm install -g appium"
    exit 1
fi

# Проверка Appium сервера
if ! lsof -i :4723 &> /dev/null; then
    echo -e "${RED}⚠️  Appium server not running on port 4723${NC}"
    echo "Start Appium: appium"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Параметры по умолчанию
PLATFORM=${1:-ios}
MARKERS=${2:-}

echo -e "${GREEN}📱 Platform: $PLATFORM${NC}"

# Запуск тестов
if [ -z "$MARKERS" ]; then
    echo -e "${GREEN}🧪 Running all tests...${NC}"
    pytest --platform "$PLATFORM" -v
else
    echo -e "${GREEN}🧪 Running tests with marker: $MARKERS${NC}"
    pytest --platform "$PLATFORM" -m "$MARKERS" -v
fi

echo ""
echo -e "${BLUE}✅ Done!${NC}"

