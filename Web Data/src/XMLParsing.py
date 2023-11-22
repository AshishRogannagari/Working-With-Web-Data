import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate


class SitemapParser:
    """
    A class to parse sitemaps of a website.

    Attributes
    ----------
    base_url : str
        The base URL of the website to parse.

    Methods
    -------
    get_robots_txt()
        Fetches the robots.txt file and extracts sitemaps.
    parse_sitemaps()
        Parses the contents of each sitemap into a DataFrame and returns the result.
    display_output(result)
        Displays the output in a nicely formatted table.
    """

    def __init__(self, base_url):
        """
        Constructs all the necessary attributes for the SitemapParser object.

        Parameters
        ----------
            base_url : str
                The base URL of the website to parse.
        """
        self.base_url = base_url
        self.sitemaps = []

    def get_robots_txt(self):
        """
        Fetches the robots.txt file and extracts sitemaps.
        """
        try:
            self.sitemaps.extend(
                line.split(": ")[1].strip()
                for line in requests.get(f"{self.base_url}/robots.txt").text.split("\n")
                if line.startswith("Sitemap:")
            )
        except requests.exceptions.RequestException as e:
            print(f"Error fetching robots.txt: {e}")

    def parse_sitemaps(self):
        """
        Parses the contents of each sitemap into a DataFrame and returns the result.

        Returns
        -------
        list
            A list of dictionaries containing the sitemap URL and its URLs.
        """
        result = []
        for sitemap_url in self.sitemaps:
            try:
                soup = BeautifulSoup(requests.get(sitemap_url).content, "xml")
                result.append(
                    {
                        "Sitemap": sitemap_url,
                        "URLs": [loc.text for loc in soup.find_all("loc")],
                    }
                )
            except requests.exceptions.RequestException as e:
                print(f"Error fetching or parsing sitemap {sitemap_url}: {e}")
        return result

    def display_output(self, result):
        """
        Displays the output in a nicely formatted table.

        Parameters
        ----------
        result : list
            A list of dictionaries containing the sitemap URL and its URLs.
        """
        for entry in result:
            df = pd.DataFrame({"URL": entry["URLs"]})
            print(f"Sitemap: {entry['Sitemap']}")
            print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
            print("\n")


if __name__ == "__main__":
    website_url = "https://www.seoptimer.com"

    # Create an instance of the SitemapParser class
    parser = SitemapParser(website_url)

    # Get the robots.txt file and extract sitemaps
    parser.get_robots_txt()

    # Parse the contents of each sitemap into a DataFrame and get the result
    result = parser.parse_sitemaps()

    # Display the output in a nicely formatted table
    parser.display_output(result)
