import textwrap
import requests
from bs4 import BeautifulSoup


class MyWikiScraper:
    """
    This class provides a scraper to fetch the content of a Wikipedia page and scrape data from it.
    """

    def __init__(self, url):
        """
        Initializes the scraper with the given Wikipedia page URL.

        :param url: The URL of the Wikipedia page to fetch.
        """
        self.url = url

    def fetch_data(self):
        """
        Fetches the content of the Wikipedia page.

        :return: The HTML content of the Wikipedia page. If the fetching fails, it returns None.
        """
        try:
            # Send a GET request to the URL
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def scrape_data(self, html_content):
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract data from the main content area
            main_content = soup.find("div", {"id": "mp-upper"})
            if not main_content:
                raise Exception("Main content area not found on the page.")

            # Extract text from paragraphs within the main content area
            paragraphs = main_content.find_all("p")
            data = [paragraph.get_text() for paragraph in paragraphs]

            return data
        except Exception as e:
            print(f"Error scraping data: {e}")
            return None

    def run(self):
        """
        Runs the scraper to fetch HTML content from the website and scrape data from it.
        """
        # Fetch HTML content from the website
        html_content = self.fetch_data()

        if html_content:
            # Scrape data from the HTML content
            scraped_data = self.scrape_data(html_content)

            if scraped_data:
                # Print or process the scraped data
                for paragraph in scraped_data:
                    # Wrap the paragraph text to a narrower width (e.g., 80 characters)
                    wrapped_paragraph = textwrap.fill(paragraph, width=80)
                    print(wrapped_paragraph)
                    print("\n" + "-" * 20 + "\n")  # Separation line
            else:
                print("No data scraped.")
        else:
            print("Failed to fetch HTML content.")


url_to_scrape = "https://en.wikipedia.org/wiki/Main_Page"
scraper = MyWikiScraper(url_to_scrape)
scraper.run()
