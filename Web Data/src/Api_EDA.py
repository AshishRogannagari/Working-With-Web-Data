import requests
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns


class ArtworksExtractor:
    """
    A class for extracting artworks data from the Art Institute of Chicago's API.

    Parameters:
    - base_url (str): The base URL of the API. Defaults to "https://api.artic.edu/api/v1/artworks".

    Methods:
    - get_artworks_data(): Fetches and returns the artworks data from the API.
    - create_dataframe(artworks_data): Converts the artworks data into a Pandas DataFrame.

    Raises:
    - requests.exceptions.HTTPError: If an HTTP error occurs during the request.
    - requests.exceptions.ConnectionError: If there is an error connecting to the API.
    - requests.exceptions.Timeout: If the request times out.
    - requests.exceptions.RequestException: If a general request exception occurs.

    Returns:
    - dict or None: A dictionary containing the artworks data if successful, otherwise None.
    - pd.DataFrame or None: A Pandas DataFrame containing the artworks data if successful, otherwise None.
    """

    def __init__(self, base_url="https://api.artic.edu/api/v1/artworks"):
        """
        Initializes an instance of the ArtworksExtractor class.

        Parameters:
        - base_url (str): The base URL of the API. Defaults to "https://api.artic.edu/api/v1/artworks".
        """
        self.base_url = base_url

    def get_artworks_data(self):
        """
        Fetches and returns the artworks data from the Art Institute of Chicago's API.

        Returns:
        - dict or None: A dictionary containing the artworks data if successful, otherwise None.
        """
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            data = response.json()
            return data["data"]
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")

        return None

    def create_dataframe(self, artworks_data):
        """
        Converts the artworks data into a Pandas DataFrame.

        Parameters:
        - artworks_data (dict or None): A dictionary containing the artworks data.

        Returns:
        - pd.DataFrame or None: A Pandas DataFrame containing the artworks data if successful, otherwise None.
        """
        if artworks_data is not None:
            return pd.DataFrame(artworks_data)
        else:
            return None


# Example usage:
# Create an instance of the ArtworksExtractor class with the default base URL.
artworks_extractor = ArtworksExtractor()

# Fetch artworks data from the Art Institute of Chicago's API.
artworks_data = artworks_extractor.get_artworks_data()

# Check if artworks data was successfully retrieved.
if artworks_data:
    # If data is available, create a Pandas DataFrame from the artworks data.
    df = artworks_extractor.create_dataframe(artworks_data)

    # Print the DataFrame containing artworks information.
    print(df)
else:
    # If retrieval of artworks data failed, print an error message.
    print("Failed to retrieve artworks data from the Art Institute of Chicago API.")


class ArtworksEDA:
    def detail():
        """
        Function used to show some of the initial content of the dataset to get an idea on how the data looks like.
        """
        return df.head()

    def summary():
        """
        Function used to show the attributes of dataset.
        """
        return df.columns

    def info():
        """
        This function shows the details of the attributes such as count of non-null values and data type.
        """
        info = df.info()
        return info

    def null_values():
        """
        Function showing the count of non-null values of each attributes.
        """
        null_values = pd.isnull(df).sum()
        return null_values

    def shape():
        """
        Function showing the dimension of the dataset.
        """
        shape = df.shape
        return shape

    def describe():
        """
        Function used to see the statistical summary of data
        """
        describe = df.describe()
        return describe

    def data_type():
        """
        Function used to see the data type of each attribute
        """
        data_type = df.dtypes
        return data_type

    def title():
        # Distribution of Title
        plt.figure(figsize=(20, 8))
        sns.histplot(df["title"], bins=20, kde=True)
        plt.title("Distribution of Title")
        plt.xticks(rotation=45, ha="right")
        plt.show()

    def plot_artwork_type_distribution():
        plt.figure(figsize=(12, 6))
        sns.countplot(
            x="artwork_type_title",
            data=df,
            order=df["artwork_type_title"].value_counts().index[:10],
        )
        plt.title("Types of Artwork  Distribution")
        plt.xticks(rotation=45, ha="right")
        plt.show()
        plt.show()

    def plot_top_artists():
        plt.figure(figsize=(12, 6))
        artist_counts = df["artist_title"].value_counts().head()
        sns.scatterplot(x=artist_counts.index, y=artist_counts.values)
        plt.title("Artists with Most artwork sales")
        plt.xticks(rotation=45, ha="right")
        plt.show()

    def plot_map_of_artworks():
        plt.figure(figsize=(12, 8))
        sns.scatterplot(
            x="longitude",
            y="latitude",
            data=df,
            hue="is_on_view",
            palette="viridis",
            alpha=0.7,
        )
        plt.title("Geographical Distribution of Artworks")
        plt.show()

    def plot_colorfulness_distribution():
        plt.figure(figsize=(12, 6))
        sns.histplot(df["colorfulness"], bins=20, kde=True)
        plt.title("Distribution of Colorfulness in Artworks")
        plt.show()
        sns.scatterplot(
            x="longitude",
            y="latitude",
            data=df,
            hue="is_on_view",
            palette="viridis",
            alpha=0.7,
        )
        plt.title("Geographical Distribution of Artworks")
        plt.show()

    def plot_colorfulness_distribution():
        plt.figure(figsize=(12, 6))
        sns.histplot(df["colorfulness"], bins=20, kde=True)
        plt.title("Distribution of Colorfulness in Artworks")
        plt.show()

    def plot_department_distribution():
        plt.figure(figsize=(10, 10))
        department_counts = df["department_title"].value_counts()
        department_counts.plot.pie(autopct="%1.1f%%", startangle=90)
        plt.title("Distribution of Artworks by Department")
        plt.show()

    def title_wordcloud():
        plt.figure(figsize=(16, 8))

        # Concatenate all titles into a single string
        titles_text = " ".join(df["title"].dropna())

        # Generate a word cloud
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            titles_text
        )

        # Display the word cloud
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Most Arts Cloud")
        plt.show()
