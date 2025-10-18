"""
Pytest configuration file с fixtures и hooks.

Содержит:
- Фикстуру для инициализации Appium сессии
- Hook для добавления опции --platform в командную строку
- Фикстуру device_manager для доступа к DeviceManager
"""

import pytest
import json
import os
import allure
from pathlib import Path
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options
from appium.options.windows import WindowsOptions

from utils.device_manager import DeviceManager
from page_objects.calculator_page import CalculatorPage


def pytest_addoption(parser):
    """
    Добавляет кастомные опции командной строки для pytest.
    
    Использование:
        pytest --platform ios
        pytest --platform android
    """
    parser.addoption(
        "--platform",
        action="store",
        default="ios",
        help="Platform to run tests on: ios, android, or windows (default: ios)"
    )
    parser.addoption(
        "--appium-server",
        action="store",
        default="http://localhost:4723",
        help="Appium server URL (default: http://localhost:4723)"
    )


def load_capabilities(platform: str) -> dict:
    """
    Загружает capabilities из JSON файла для указанной платформы.
    
    Args:
        platform: Название платформы ('ios', 'android', 'windows')
        
    Returns:
        Dictionary с capabilities
        
    Raises:
        FileNotFoundError: Если файл конфигурации не найден
    """
    config_dir = Path(__file__).parent / "config"
    config_file = config_dir / f"{platform.lower()}.json"
    
    if not config_file.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_file}\n"
            f"Available platforms: ios, android, windows"
        )
    
    with open(config_file, 'r', encoding='utf-8') as f:
        capabilities = json.load(f)
    
    return capabilities


def create_driver(platform: str, appium_server: str) -> webdriver.Remote:
    """
    Создает Appium driver на основе платформы и capabilities.
    
    Args:
        platform: Название платформы
        appium_server: URL Appium сервера
        
    Returns:
        Appium WebDriver instance
    """
    caps = load_capabilities(platform)
    
    # Создаем опции в зависимости от платформы
    if platform.lower() == 'ios':
        options = XCUITestOptions()
        options.platform_name = caps.get('platformName', 'iOS')
        options.platform_version = caps.get('platformVersion')
        options.device_name = caps.get('deviceName')
        options.automation_name = caps.get('automationName', 'XCUITest')
        options.bundle_id = caps.get('bundleId')
        options.udid = caps.get('udid', 'auto')
        options.no_reset = caps.get('noReset', False)
        options.full_reset = caps.get('fullReset', False)
        options.new_command_timeout = caps.get('newCommandTimeout', 300)
        options.wda_launch_timeout = caps.get('wdaLaunchTimeout', 120000)
        options.wda_connection_timeout = caps.get('wdaConnectionTimeout', 120000)
        options.use_new_wda = caps.get('useNewWDA', False)
        options.use_prebuilt_wda = caps.get('usePrebuiltWDA', True)
        
        # Settings
        if 'settings' in caps:
            for key, value in caps['settings'].items():
                options.set_capability(f'settings[{key}]', value)
    
    elif platform.lower() == 'android':
        options = UiAutomator2Options()
        options.platform_name = caps.get('platformName', 'Android')
        options.platform_version = caps.get('platformVersion')
        options.device_name = caps.get('deviceName')
        options.automation_name = caps.get('automationName', 'UiAutomator2')
        options.app_package = caps.get('appPackage')
        options.app_activity = caps.get('appActivity')
        options.udid = caps.get('udid', 'auto')
        options.no_reset = caps.get('noReset', False)
        options.full_reset = caps.get('fullReset', False)
        options.new_command_timeout = caps.get('newCommandTimeout', 300)
        options.auto_grant_permissions = caps.get('autoGrantPermissions', True)
        
        # Settings
        if 'settings' in caps:
            for key, value in caps['settings'].items():
                options.set_capability(f'settings[{key}]', value)
    
    elif platform.lower() == 'windows':
        options = WindowsOptions()
        options.platform_name = caps.get('platformName', 'Windows')
        options.device_name = caps.get('deviceName', 'WindowsPC')
        options.app = caps.get('app')
        options.automation_name = caps.get('automationName', 'Windows')
        options.new_command_timeout = caps.get('newCommandTimeout', 300)
    
    else:
        raise ValueError(f"Unsupported platform: {platform}")
    
    # Создаем driver
    driver = webdriver.Remote(appium_server, options=options)
    
    return driver


@pytest.fixture(scope="session")
def platform(request) -> str:
    """
    Fixture для получения платформы из командной строки.
    
    Returns:
        Название платформы (ios, android, windows)
    """
    return request.config.getoption("--platform")


@pytest.fixture(scope="session")
def appium_server_url(request) -> str:
    """
    Fixture для получения URL Appium сервера.
    
    Returns:
        URL Appium сервера
    """
    return request.config.getoption("--appium-server")


@pytest.fixture(scope="session")
def device_manager(platform, appium_server_url) -> DeviceManager:
    """
    Fixture для инициализации DeviceManager с Appium driver.
    
    Создает Appium сессию один раз на всю session, инициализирует DeviceManager.
    НЕ запускает приложение (запуск происходит в function-scoped fixture app).
    После всех тестов закрывает сессию.
    
    Args:
        platform: Платформа для тестирования
        appium_server_url: URL Appium сервера
        
    Yields:
        DeviceManager instance
    """
    # Создаем driver
    driver = create_driver(platform, appium_server_url)
    
    # Получаем bundle ID или package name из capabilities
    caps = load_capabilities(platform)
    if platform.lower() == 'ios':
        app_id = caps.get('bundleId')
    elif platform.lower() == 'android':
        app_id = caps.get('appPackage')
    else:
        app_id = None
    
    # Инициализируем DeviceManager
    dm = DeviceManager()
    dm.initialize_driver(driver, platform, app_id)
    
    # НЕ запускаем приложение здесь - это делает fixture app перед каждым тестом
    
    yield dm
    
    # Teardown: закрываем сессию после всех тестов
    try:
        dm.close_app()
    except Exception as e:
        print(f"Warning: Error closing app: {e}")
    finally:
        # Сбрасываем singleton instance
        DeviceManager.reset_instance()


@pytest.fixture(scope="function")
def calculator(device_manager, screenshot_on_failure) -> CalculatorPage:
    """
    Function-scoped fixture для работы с калькулятором в тестах.
    
    Запускает приложение перед каждым тестом и останавливает после.
    Обеспечивает полную изоляцию тестов - каждый тест начинается 
    с чистого состояния приложения в портретной ориентации (установлено через capabilities).
    
    Args:
        device_manager: Session-scoped DeviceManager
        
    Yields:
        CalculatorPage instance для работы с UI калькулятора
    """
    # Setup: Запускаем приложение перед каждым тестом
    # Ориентация устанавливается через capabilities, но принудительно проверяем/устанавливаем PORTRAIT
    if device_manager.is_app_running():
        device_manager.stop_app()
    
    # Принудительно устанавливаем портретную ориентацию перед запуском приложения
    if not device_manager.is_portrait():
        device_manager.rotate_to_portrait(wait_for_ui=False)
    
    device_manager.start_app()
    
    # Создаем и возвращаем объект CalculatorPage
    calc_page = CalculatorPage()
    
    yield calc_page
    
    # Teardown: Останавливаем приложение после каждого теста
    if device_manager.is_app_running():
        device_manager.stop_app()


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, device_manager):
    """
    Fixture для автоматического создания скриншота при падении теста.
    Скриншот сохраняется локально и прикрепляется к Allure отчету.
    
    Использование:
        def test_something(screenshot_on_failure, app):
            # Тест автоматически сделает скриншот при падении
            pass
    """
    yield
    
    # После выполнения теста проверяем, упал ли он
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        try:
            test_name = request.node.name
            screenshot_dir = Path(__file__).parent / "screenshots"
            screenshot_dir.mkdir(exist_ok=True)
            
            screenshot_path = screenshot_dir / f"{test_name}_failure.png"
            device_manager.take_screenshot(str(screenshot_path))
            print(f"\n📸 Screenshot saved: {screenshot_path}")
            
            # Прикрепляем скриншот к Allure отчету
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=f"Screenshot: {test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"\n⚠️ Could not save screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook для сохранения результата теста в объекте request.
    Используется в fixture screenshot_on_failure.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

