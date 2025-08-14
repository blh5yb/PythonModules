import requests
from bs4 import BeautifulSoup
from src.shared import *

########################################################################################################################
# Static Web Scraping Module
# Author: Barry Hykes Jr, bhykes@gmail.com
# version 1.0.0
########################################################################################################################

class StaticWebScraper:
    """Static HTML Web Scraper Module"""
    def __init__(cls, url):
        """
        Fetch static html
        :param url: website to scrape, str
        """
        cls.url = url
        try:
            self.__response = requests.get(url)
            logger.info(f'Initializing StaticWebScraper')
        except Exception as e:
            logger.error(f"Error fetching url, {url}: {e}")
            raise
            # print(self.soup.prettify())

    def extract_static_content(self, tag, attributes):
        """
        parse html to get html matching the query attributes
        :param tag: html tag to query, str
        :param attributes: attributes to filter on (i.e. {'id': 'my_id'}), dict
        :return content_div: html content found, bytes str
        """
        try:
            soup = BeautifulSoup(self.__response.content, 'html.parser')
            content_div = soup.find(tag, attrs=attributes)
            return content_div
        except Exception as e:
            logger.error(f"failed to find {tag} tag with {attributes} attributes: {e}")
            raise


def main(args):
    # 'https://barryhightech.org/home'
    StaticWebScraper(args.url)
    scraping = StaticWebScraper(args.url)
    scraping.extract_static_content('div', {'id', 'my_id'})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Web Scraping module")
    parser.add_argument('-u', '--url', type=str, action="store", required=True, help="full url path")
    parser_args = parser.parse_args()
    main(parser_args)