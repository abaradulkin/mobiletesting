#!/usr/bin/env python3
"""
Скрипт для проверки настройки Android окружения.

Проверяет:
- Наличие adb
- Подключенные Android устройства
- Установлен ли Google Calculator
- Доступность Appium сервера
- Возможность создания сессии
"""

import subprocess
import sys
import json
import requests
from pathlib import Path


def check_adb():
    """Проверяет наличие adb в системе."""
    print("\n🔍 Проверка ADB...")
    try:
        result = subprocess.run(['adb', 'version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            print(f"✅ ADB найден: {result.stdout.split()[4]}")
            return True
        else:
            print("❌ ADB не найден или не работает")
            return False
    except FileNotFoundError:
        print("❌ ADB не установлен")
        print("💡 Установите Android SDK и добавьте platform-tools в PATH")
        return False
    except Exception as e:
        print(f"❌ Ошибка при проверке ADB: {e}")
        return False


def check_devices():
    """Проверяет подключенные Android устройства."""
    print("\n🔍 Проверка подключенных устройств...")
    try:
        result = subprocess.run(['adb', 'devices'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        
        lines = result.stdout.strip().split('\n')[1:]  # Пропускаем первую строку "List of devices"
        devices = [line.split()[0] for line in lines if line.strip() and 'device' in line]
        
        if devices:
            print(f"✅ Найдено устройств: {len(devices)}")
            for device in devices:
                print(f"   📱 {device}")
            return devices
        else:
            print("❌ Нет подключенных Android устройств")
            print("💡 Подключите устройство или запустите эмулятор")
            return []
    except Exception as e:
        print(f"❌ Ошибка при проверке устройств: {e}")
        return []


def check_calculator_installed(device_id):
    """Проверяет, установлен ли Google Calculator."""
    print(f"\n🔍 Проверка Google Calculator на устройстве {device_id}...")
    try:
        result = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'pm', 'list', 'packages', 'com.google.android.calculator'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if 'com.google.android.calculator' in result.stdout:
            print("✅ Google Calculator установлен")
            return True
        else:
            print("❌ Google Calculator НЕ установлен")
            print("💡 Установите из Google Play Store")
            return False
    except Exception as e:
        print(f"❌ Ошибка при проверке Calculator: {e}")
        return False


def check_appium_server():
    """Проверяет доступность Appium сервера."""
    print("\n🔍 Проверка Appium сервера...")
    try:
        response = requests.get('http://localhost:4723/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Appium сервер запущен")
            print(f"   Версия: {data.get('value', {}).get('build', {}).get('version', 'unknown')}")
            return True
        else:
            print("❌ Appium сервер не отвечает")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Appium сервер не запущен")
        print("💡 Запустите: appium")
        return False
    except Exception as e:
        print(f"❌ Ошибка при проверке Appium: {e}")
        return False


def check_config():
    """Проверяет конфигурационный файл."""
    print("\n🔍 Проверка config/android.json...")
    config_path = Path(__file__).parent / 'config' / 'android.json'
    
    if not config_path.exists():
        print("❌ Файл config/android.json не найден")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print("✅ Конфигурация найдена:")
        print(f"   Platform: {config.get('platformName')}")
        print(f"   App Package: {config.get('appPackage')}")
        print(f"   App Activity: {config.get('appActivity')}")
        print(f"   Automation: {config.get('automationName')}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при чтении конфигурации: {e}")
        return False


def main():
    """Основная функция проверки."""
    print("=" * 60)
    print("🤖 Проверка Android окружения для Mobile Testing")
    print("=" * 60)
    
    results = {
        'adb': check_adb(),
        'config': check_config(),
        'devices': check_devices(),
        'appium': check_appium_server()
    }
    
    if results['devices']:
        device_id = results['devices'][0]
        results['calculator'] = check_calculator_installed(device_id)
    else:
        results['calculator'] = False
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ")
    print("=" * 60)
    
    all_passed = all([
        results['adb'],
        results['config'],
        bool(results['devices']),
        results['appium'],
        results['calculator']
    ])
    
    if all_passed:
        print("✅ ВСЁ ГОТОВО! Можно запускать тесты на Android")
        print("\n💡 Команда для запуска:")
        print("   pytest --platform android -m smoke -v")
    else:
        print("❌ Есть проблемы, которые нужно исправить:")
        if not results['adb']:
            print("   - Установите Android SDK и adb")
        if not results['devices']:
            print("   - Подключите устройство или запустите эмулятор")
        if not results['appium']:
            print("   - Запустите Appium сервер")
        if not results['calculator']:
            print("   - Установите Google Calculator")
    
    print("=" * 60)
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())

