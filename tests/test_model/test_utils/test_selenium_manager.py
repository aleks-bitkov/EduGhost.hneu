from unittest.mock import Mock, patch

import pytest
from selenium.webdriver.firefox.service import Service as ServiceFirefox

from app.model.utils.selenium_manager import SeleniumManager


class TestBrowserManager:
    
    @pytest.fixture
    def selenium_manager(self):
        """Фикстура для создания экземпляра BrowserManager"""
        return SeleniumManager()
    
    def test_init(self, selenium_manager):
        """Тест инициализации SeleniumManager"""
        assert selenium_manager._driver is None
        assert isinstance(selenium_manager._service, ServiceFirefox)
        assert selenium_manager._options is not None
    
    def test_is_driver_available_when_no_driver(self, selenium_manager):
        """Тест is_driver_available когда драйвер не создан"""
        assert selenium_manager.is_driver_available() is False
    
    def test_is_driver_available_when_driver_exists(self, selenium_manager):
        """Тест is_driver_available когда драйвер существует"""
        selenium_manager._driver = Mock()
        assert selenium_manager.is_driver_available() is True
    
    @pytest.mark.asyncio
    @patch('app.model.utils.selenium_manager.webdriver.Firefox')
    async def test_driver_property_creates_new_driver(self, mock_firefox, selenium_manager):
        """Тест создания нового драйвера через свойство driver"""
        mock_driver_instance = Mock()
        mock_firefox.return_value = mock_driver_instance
        
        driver = await selenium_manager.driver
        
        assert driver == mock_driver_instance
        assert selenium_manager._driver == mock_driver_instance
        mock_firefox.assert_called_once_with(
            service=selenium_manager._service,
            options=selenium_manager._options
        )
    
    @pytest.mark.asyncio
    async def test_driver_property_returns_existing_driver(self, selenium_manager):
        """Тест возврата существующего драйвера"""
        existing_driver = Mock()
        selenium_manager._driver = existing_driver
        
        driver = await selenium_manager.driver
        
        assert driver == existing_driver
    
    @pytest.mark.asyncio
    async def test_close_when_driver_exists(self, selenium_manager):
        """Тест закрытия драйвера когда он существует"""
        mock_driver = Mock()
        selenium_manager._driver = mock_driver
        
        await selenium_manager.close()
        
        mock_driver.quit.assert_called_once()
        assert selenium_manager._driver is None
    
    @pytest.mark.asyncio
    async def test_close_when_no_driver(self, selenium_manager):
        """Тест закрытия когда драйвер не существует"""
        selenium_manager._driver = None
        
        # Не должно вызывать исключений
        await selenium_manager.close()
        
        assert selenium_manager._driver is None
    
    @pytest.mark.asyncio
    @patch('app.model.utils.selenium_manager.webdriver.Firefox')
    async def test_full_workflow(self, mock_firefox, selenium_manager):
        """Тест полного рабочего цикла"""
        mock_driver_instance = Mock()
        mock_firefox.return_value = mock_driver_instance
        
        # Проверяем, что драйвер недоступен
        assert not selenium_manager.is_driver_available()
        
        # Создаем драйвер
        driver = await selenium_manager.driver
        assert selenium_manager.is_driver_available()
        assert driver == mock_driver_instance
        
        # Закрываем драйвер
        await selenium_manager.close()
        assert not selenium_manager.is_driver_available()
        mock_driver_instance.quit.assert_called_once()


# Дополнительные тесты для обработки ошибок
class TestBrowserManagerErrorHandling:
    
    @pytest.mark.asyncio
    @patch('app.model.utils.selenium_manager.webdriver.Firefox')
    async def test_driver_creation_failure(self, mock_firefox):
        """Тест обработки ошибки при создании драйвера"""
        mock_firefox.side_effect = Exception("Firefox not found")
        selenium_manager = SeleniumManager()
        
        with pytest.raises(Exception, match="Firefox not found"):
            await selenium_manager.driver
    
    @pytest.mark.asyncio
    async def test_close_with_driver_quit_error(self):
        """Тест обработки ошибки при закрытии драйвера"""
        selenium_manager = SeleniumManager()
        mock_driver = Mock()
        mock_driver.quit.side_effect = Exception("Quit failed")
        selenium_manager._driver = mock_driver
        
        # Должно вызвать исключение
        with pytest.raises(Exception, match="Quit failed"):
            await selenium_manager.close()
