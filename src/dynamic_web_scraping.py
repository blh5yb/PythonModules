from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from src.shared import *
########################################################################################################################
# Dynamic Scraping Modules
# Author: Barry Hykes Jr, bhykes@gmail.com
# version 1.0.0
########################################################################################################################


class ChromeScraper:
    """Dynamic Javascript Web Scraper Module"""
    def __init__(self, url):
        """
        Initialize dynamic web scraping chrome driver
        :param url: website to scrape, str
        """
        try:
            options = webdriver.ChromeOptions()
            # Runs the browser in the background without opening a visible window — ideal for automation and speed.
            options.add_argument("--headless")  # Run in headless mode (optional)
            # Automatically downloads the correct version of ChromeDriver based on your Chrome browser.
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            service = Service(ChromeDriverManager().install())
            self.__driver = webdriver.Chrome(service=service, options=options)
            self.__driver.get(url)
            time.sleep(1) # Optional wait to ensure page loads
            print('url', url)
            logger.info(f'loaded chrome driver: {url}')

        except Exception as e:
            logger.error(f"Chrome Driver Initialization Error: {e}")
            raise

    def extract_elements_by_id(self, tag):
        """
        Find elements by ID
        :param tag: ID of the elements to fetch, str
        :return elements: html elements found by driver, array
        """
        try:
            elements = self.__driver.find_elements(By.ID, tag)
            logger.info(f"found {len(elements)} html elements with id, {tag}")
            return elements

        except Exception as e:
            logger.error(f"Error searching for element with tag {tag} by id: {e}")
            raise

    def extract_elements_by_class_name(self, tag):
        """
        Find elements by Class Name
        :param tag: Class Name of the elements to fetch, str
        :return elements: html elements found by driver, array
        """
        try:
            elements = self.__driver.find_elements(By.CLASS_NAME, tag)
            logger.info(f"found {len(elements)} html elements with class name, {tag}")
            return elements

        except Exception as e:
            logger.error(f"Error searching for element with tag {tag} by class name: {e}")
            raise

    def close(self):
        """Close the driver"""
        self.__driver.quit()
        logger.info("Chrome Driver is closed")

def main(args):
    # 'https://barryhightech.org/home'
    # scraping = StaticWebScraper(args.url)
    # scraping.extract_static_content('div', {'id', 'my_id'})
    chrome_scraping = ChromeScraper(args.url)
    chrome_scraping.extract_elements_by_class_name('text-header-sm')
    # elements = chrome_scraping.extract_elements_by_class_name('image-center')
    # elements = chrome_scraping.extract_elements_by_class_name('ion-text-center')
    # print('elements', elements)
    # # Get the outer HTML of the element
    # outer_html = elements[0].get_attribute('outerHTML')
    # print("Outer HTML:", outer_html)
    #
    # # Get the inner HTML of the element
    # inner_html = elements[0].get_attribute('innerHTML')
    # print("Inner HTML:", inner_html)
    chrome_scraping.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Web Scraping module")
    parser.add_argument('-u', '--url', type=str, action="store", required=True, help="full url path")
    parser_args = parser.parse_args()
    main(parser_args)