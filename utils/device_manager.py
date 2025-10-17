"""
DeviceManager - Singleton класс для управления Appium сессией и устройством.

Предоставляет единую точку доступа к Appium driver и методы для управления
приложением и устройством из любой части тестового фреймворка.
"""

from typing import Optional
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import WebDriverException
import logging

logger = logging.getLogger(__name__)


class DeviceManager:
    """
    Singleton класс для управления Appium сессией и устройством.
    
    Обеспечивает:
    - Единственный экземпляр для всего тестового фреймворка
    - Управление жизненным циклом приложения
    - Управление состоянием устройства (ориентация, сеть)
    - Доступ к Appium driver из любой точки кода
    """
    
    _instance: Optional['DeviceManager'] = None
    _driver: Optional[webdriver.Remote] = None
    _platform: Optional[str] = None
    _app_bundle_id: Optional[str] = None
    
    def __new__(cls):
        """
        Реализация паттерна Singleton.
        Гарантирует создание только одного экземпляра класса.
        """
        if cls._instance is None:
            cls._instance = super(DeviceManager, cls).__new__(cls)
            logger.info("DeviceManager instance created")
        return cls._instance
    
    def initialize_driver(
        self,
        driver: webdriver.Remote,
        platform: str,
        app_bundle_id: str = None
    ) -> None:
        """
        Инициализирует Appium driver в DeviceManager.
        
        Args:
            driver: Экземпляр Appium WebDriver
            platform: Название платформы ('ios' или 'android')
            app_bundle_id: Bundle ID приложения (для iOS) или package name (для Android)
        """
        self._driver = driver
        self._platform = platform.lower()
        self._app_bundle_id = app_bundle_id
        logger.info(f"Driver initialized for platform: {self._platform}")
    
    @property
    def driver(self) -> webdriver.Remote:
        """
        Возвращает экземпляр Appium driver.
        
        Returns:
            Appium WebDriver instance
            
        Raises:
            RuntimeError: Если driver не был инициализирован
        """
        if self._driver is None:
            raise RuntimeError(
                "Driver not initialized. Call initialize_driver() first."
            )
        return self._driver
    
    @property
    def platform(self) -> str:
        """Возвращает название платформы."""
        return self._platform
    
    # ==================== Управление приложением ====================
    
    def start_app(self) -> None:
        """
        Запускает приложение на устройстве.
        """
        try:
            if self._platform == 'ios':
                if self._app_bundle_id:
                    self._driver.activate_app(self._app_bundle_id)
                    logger.info(f"iOS app started: {self._app_bundle_id}")
                else:
                    logger.warning("Bundle ID not provided, cannot start app")
            elif self._platform == 'android':
                # Для Android можно использовать driver.start_activity
                # или activate_app если известен package name
                if self._app_bundle_id:
                    self._driver.activate_app(self._app_bundle_id)
                    logger.info(f"Android app started: {self._app_bundle_id}")
                else:
                    logger.warning("Package name not provided, cannot start app")
        except WebDriverException as e:
            logger.error(f"Failed to start app: {e}")
            raise
    
    def stop_app(self) -> None:
        """
        Останавливает приложение на устройстве.
        """
        try:
            if self._app_bundle_id:
                self._driver.terminate_app(self._app_bundle_id)
                logger.info(f"App stopped: {self._app_bundle_id}")
            else:
                logger.warning("Bundle ID/Package name not provided")
        except WebDriverException as e:
            logger.error(f"Failed to stop app: {e}")
            raise
    
    def restart_app(self) -> None:
        """
        Перезапускает приложение (stop + start).
        """
        logger.info("Restarting app...")
        self.stop_app()
        self.start_app()
    
    def is_app_running(self) -> bool:
        """
        Проверяет, запущено ли приложение.
        
        Returns:
            True если приложение запущено, False иначе
        """
        if not self._app_bundle_id:
            logger.warning("Bundle ID/Package name not provided")
            return False
        
        try:
            if self._platform == 'ios':
                # Для iOS используем query_app_state
                # 4 = running in foreground
                state = self._driver.query_app_state(self._app_bundle_id)
                return state == 4
            elif self._platform == 'android':
                # Для Android проверяем current activity
                current_activity = self._driver.current_activity
                return self._app_bundle_id in current_activity
        except WebDriverException as e:
            logger.error(f"Failed to check app state: {e}")
            return False
    
    def background_app(self, seconds: int = 5) -> None:
        """
        Отправляет приложение в фон на указанное время.
        
        Args:
            seconds: Количество секунд в фоне
        """
        try:
            self._driver.background_app(seconds)
            logger.info(f"App sent to background for {seconds} seconds")
        except WebDriverException as e:
            logger.error(f"Failed to background app: {e}")
            raise
    
    # ==================== Управление устройством ====================
    
    def rotate_to_landscape(self) -> None:
        """Поворачивает устройство в landscape ориентацию."""
        try:
            self._driver.orientation = "LANDSCAPE"
            logger.info("Device rotated to LANDSCAPE")
        except WebDriverException as e:
            logger.error(f"Failed to rotate to landscape: {e}")
            raise
    
    def rotate_to_portrait(self) -> None:
        """Поворачивает устройство в portrait ориентацию."""
        try:
            self._driver.orientation = "PORTRAIT"
            logger.info("Device rotated to PORTRAIT")
        except WebDriverException as e:
            logger.error(f"Failed to rotate to portrait: {e}")
            raise
    
    def get_orientation(self) -> str:
        """
        Возвращает текущую ориентацию устройства.
        
        Returns:
            'PORTRAIT' или 'LANDSCAPE'
        """
        return self._driver.orientation
    
    def toggle_wifi(self, enable: bool = None) -> None:
        """
        Включает или выключает WiFi.
        
        Args:
            enable: True для включения, False для выключения,
                   None для переключения текущего состояния
        """
        try:
            if self._platform == 'android':
                # Для Android используем set_network_connection
                from appium.webdriver.extensions.android.network import NetConnectionType
                
                if enable is None:
                    # Toggle: получаем текущее состояние и инвертируем
                    current = self._driver.network_connection
                    enable = not bool(current & NetConnectionType.WIFI_MASK)
                
                if enable:
                    self._driver.set_network_connection(NetConnectionType.WIFI_ONLY)
                    logger.info("WiFi enabled")
                else:
                    self._driver.set_network_connection(NetConnectionType.AIRPLANE_MODE)
                    logger.info("WiFi disabled")
            else:
                logger.warning("WiFi control not supported for iOS in Appium")
        except Exception as e:
            logger.error(f"Failed to toggle WiFi: {e}")
            raise
    
    def toggle_airplane_mode(self, enable: bool = None) -> None:
        """
        Включает или выключает режим полета (только Android).
        
        Args:
            enable: True для включения, False для выключения,
                   None для переключения текущего состояния
        """
        try:
            if self._platform == 'android':
                from appium.webdriver.extensions.android.network import NetConnectionType
                
                if enable:
                    self._driver.set_network_connection(NetConnectionType.AIRPLANE_MODE)
                    logger.info("Airplane mode enabled")
                else:
                    self._driver.set_network_connection(NetConnectionType.ALL_NETWORK_ON)
                    logger.info("Airplane mode disabled")
            else:
                logger.warning("Airplane mode control not supported for iOS in Appium")
        except Exception as e:
            logger.error(f"Failed to toggle airplane mode: {e}")
            raise
    
    def toggle_mobile_data(self, enable: bool = None) -> None:
        """
        Включает или выключает мобильные данные (только Android).
        
        Args:
            enable: True для включения, False для выключения
        """
        try:
            if self._platform == 'android':
                from appium.webdriver.extensions.android.network import NetConnectionType
                
                if enable:
                    self._driver.set_network_connection(NetConnectionType.DATA_ONLY)
                    logger.info("Mobile data enabled")
                else:
                    self._driver.set_network_connection(NetConnectionType.AIRPLANE_MODE)
                    logger.info("Mobile data disabled")
            else:
                logger.warning("Mobile data control not supported for iOS in Appium")
        except Exception as e:
            logger.error(f"Failed to toggle mobile data: {e}")
            raise
    
    # ==================== Дополнительные утилиты ====================
    
    def take_screenshot(self, filename: str = None) -> str:
        """
        Делает скриншот экрана.
        
        Args:
            filename: Имя файла для сохранения (опционально)
            
        Returns:
            Путь к сохраненному скриншоту
        """
        try:
            if filename:
                screenshot_path = self._driver.save_screenshot(filename)
            else:
                screenshot_path = self._driver.get_screenshot_as_file(
                    f"screenshot_{self._platform}.png"
                )
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except WebDriverException as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise
    
    def get_page_source(self) -> str:
        """
        Возвращает XML page source текущего экрана.
        
        Returns:
            XML page source как строка
        """
        try:
            return self._driver.page_source
        except WebDriverException as e:
            logger.error(f"Failed to get page source: {e}")
            raise
    
    def reset(self) -> None:
        """
        Сбрасывает состояние приложения (переустановка).
        """
        try:
            self._driver.reset()
            logger.info("App reset completed")
        except WebDriverException as e:
            logger.error(f"Failed to reset app: {e}")
            raise
    
    def close_app(self) -> None:
        """
        Закрывает приложение и завершает driver сессию.
        """
        try:
            if self._driver:
                self._driver.quit()
                logger.info("Driver session closed")
                self._driver = None
        except WebDriverException as e:
            logger.error(f"Failed to close driver: {e}")
            raise
    
    @classmethod
    def reset_instance(cls) -> None:
        """
        Сбрасывает Singleton instance (для тестирования).
        """
        if cls._instance and cls._instance._driver:
            cls._instance.close_app()
        cls._instance = None
        cls._driver = None
        cls._platform = None
        cls._app_bundle_id = None
        logger.info("DeviceManager instance reset")

