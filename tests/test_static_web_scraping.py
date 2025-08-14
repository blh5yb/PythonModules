from src.static_web_scraping import *
from tests.custom_fixtures import pytest, patch, Mock


@pytest.fixture(scope="function")
def get_request_fixture():
    print("set up get request fixture")
    with patch('src.static_web_scraping.requests.get') as mock_req:
        mock_res = Mock()
        mock_res.content = b"<html><body><h1 class='title' id='my_id'>Scraped Title</h1></body></html>"
        mock_res.status = 200
        mock_req.return_value = mock_res
        yield mock_req

class TestStaticWebScraper:
    def setup_class(cls):
        # cls.mock_req = get_request_fixture
        # cls.mock_response = Mock()
        # mock_content = b"<html><body><h1 class='title' id='my_id'>Scraped Title</h1></body></html>"
        # cls.mock_response.status_code = 200
        # cls.mock_response.content = mock_content
        cls.url = 'https://some_url.site/home'

    def test_constructor(self, get_request_fixture):
        # get_request_fixture.return_value = self.mock_response
        # requests_mock.get(url, text=mock_content, status_code=200)
        StaticWebScraper(self.url)
        get_request_fixture.assert_called_with(self.url)

    def test_failed_req_fetch(self, get_request_fixture):
        get_request_fixture.side_effect = Exception("Failed URL Fetch")
        with pytest.raises(Exception) as e:
            StaticWebScraper(self.url)
            assert e.value == "Failed URL Fetch"

    def test_extract_content(self, get_request_fixture):
        # get_request_fixture.return_value = self.mock_response
        static_scraper = StaticWebScraper(self.url)
        res = static_scraper.extract_static_content('h1', {'class': 'title'})
        assert f'{res}' == '<h1 class="title" id="my_id">Scraped Title</h1>'

    @patch('src.static_web_scraping.BeautifulSoup')
    def test_static_exception(self, mock_soup, get_request_fixture):
        # get_request_fixture.return_value = self.mock_response
        get_request_fixture.return_value.status_code = 400
        mock_soup.side_effect = Exception('Beautiful Soup Exception')
        with pytest.raises(Exception) as e:
            static_scraper = StaticWebScraper(self.url)
            static_scraper.extract_static_content('h1', {'class': 'title'})
            assert e.value == 'Beautiful Soup Exception'