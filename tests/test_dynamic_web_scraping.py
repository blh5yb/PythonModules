
# from urllib3 import request

from tests.custom_fixtures import pytest, patch, Mock
from src.dynamic_web_scraping import *


@pytest.fixture(scope="function")
def mock_chrome_options():
    with patch('src.dynamic_web_scraping.webdriver.ChromeOptions') as options_mock:
        options_mock.return_value.add_argument = Mock()
        yield options_mock

@pytest.fixture(scope="class")
def mock_chrome_driver_manager():
    with patch('src.dynamic_web_scraping.ChromeDriverManager') as chrome_manager_mock:
        chrome_manager_mock.return_value.install.return_value = Mock()
        yield chrome_manager_mock

@pytest.fixture(scope="class")
def mock_service():
    with patch('src.dynamic_web_scraping.Service') as service_mock:
        yield service_mock

@pytest.fixture(scope="function")
def mock_chrome_driver():
    with patch('src.dynamic_web_scraping.webdriver') as chrome_driver_mock:
        chrome_driver_mock.ChromeOptions = Mock()
        chrome_driver_mock.ChromeOptions.return_value.add_argument = Mock()
        chrome_driver_mock.Chrome = Mock()
        chrome_driver_mock.Chrome.return_value.get = Mock()
        chrome_driver_mock.Chrome.return_value.quit = Mock()
        # chrome_driver_mock.Chrome.return_value.find_elements.return_value = elements

        yield chrome_driver_mock

@pytest.fixture(scope="class")
def mock_sleep():
    """Mocking time sleep to skip 1 sec delay in testing"""
    with patch('src.dynamic_web_scraping.time.sleep') as sleep_mock:
        sleep_mock.return_value = Mock()
        yield sleep_mock

class TestChromeDynamicScraper:
    @classmethod
    def setup_class(cls):
        """Could use global variable but using class method just for reference of another way"""
        cls.url = 'https://some_url.site/home'
        cls.html = "<html><body><h1 class='title' id='my_id'>Scraped Title</h1></body></html>"
        cls.id = 'my_id'
        cls.class_name = 'title'
        cls.elements = [Mock()]
        for el in cls.elements:
            el.text = 'Scraped Title'
            el.get_attribute.return_value = "<body><h1 class='title' id='my_id'>Scraped Title</h1></body>"
            # el.innerHTML = "<h1 class='title' id='my_id'>Scraped Title</h1>"
            # el.outerHTML = "<body><h1 class='title' id='my_id'>Scraped Title</h1></body>"

    def test_constructor(self, mock_chrome_driver_manager, mock_service, mock_chrome_driver, mock_sleep):
        """Test initializing the chrome web driver for the url"""
        ChromeScraper(self.url)
        assert mock_chrome_driver_manager.return_value.install.call_count == 1
        assert mock_service.call_count == 1
        assert mock_sleep.call_count == 1
        assert mock_chrome_driver.ChromeOptions.return_value.add_argument.call_count == 3
        mock_chrome_driver.Chrome.return_value.get.assert_called_with(self.url)

    def test_constructor_exception(self, mock_chrome_driver_manager, mock_service, mock_chrome_driver, mock_sleep):
        mock_chrome_driver.ChromeOptions.side_effect = Exception('ChromeOptions Exception')
        with pytest.raises(Exception) as e:
            ChromeScraper(self.url)
            assert e.value == 'ChromeOptions Exception'

    def test_extract_by_id(self, mock_chrome_driver_manager, mock_service, mock_chrome_driver, mock_sleep):
        chrome_scraper = ChromeScraper(self.url)
        mock_chrome_driver.Chrome.return_value.find_elements.return_value = self.elements
        result = chrome_scraper.extract_elements_by_id(self.id)
        assert result == self.elements
        mock_chrome_driver.Chrome.return_value.find_elements.assert_called()

    def test_extract_by_id_exception(self, mock_chrome_driver_manager, mock_service, mock_chrome_driver, mock_sleep):
        mock_chrome_driver.Chrome.return_value.find_elements.side_effect = Exception('Find By Id exception')
        with pytest.raises(Exception) as e:
            chrome_scraper = ChromeScraper(self.url)
            chrome_scraper.extract_elements_by_id(self.id)
            assert e.value == 'Find By Id exception'

    def test_extract_by_class(self, mock_chrome_driver_manager, mock_service, mock_chrome_driver, mock_sleep):
        chrome_scraper = ChromeScraper(self.url)
        mock_chrome_driver.Chrome.return_value.find_elements.return_value = self.elements
        result = chrome_scraper.extract_elements_by_class_name(self.class_name)
        assert result == self.elements
        mock_chrome_driver.Chrome.return_value.find_elements.assert_called()

    def test_extract_by_class_exception(self, mock_chrome_driver_manager, mock_service, mock_chrome_driver, mock_sleep):
        mock_chrome_driver.Chrome.return_value.find_elements.side_effect = Exception('Find By ClassName exception')
        with pytest.raises(Exception) as e:
            chrome_scraper = ChromeScraper(self.url)
            chrome_scraper.extract_elements_by_class_name(self.class_name)
            assert e.value == 'Find By ClassName exception'

    def test_close_driver(self, mock_chrome_driver_manager, mock_service, mock_chrome_driver, mock_sleep):

        chrome_scraper = ChromeScraper(self.url)
        chrome_scraper.close()
        mock_chrome_driver.Chrome.return_value.quit.assert_called()

