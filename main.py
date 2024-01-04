import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_paper_urls(source_url):
    paper_urls = []

    try:
        response = requests.get(source_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links containing "#paper"
        for link in soup.find_all('a', href=True):
            href = link['href']
            if "#paper" in href:
                full_url = urljoin(source_url, href)
                paper_urls.append(full_url)

        return paper_urls

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def modify_urls(urls):
    modified_urls = []
    for url in urls:
        modified_url = url.replace("/deck/", "/deck/download/").replace("#paper", "")
        modified_urls.append(modified_url)
    return modified_urls
def download_files(urls, download_folder="."):
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Extract the filename from the URL
            filename = url.split("/")[-1]

            # Save the content to a file in the specified download folder
            with open(os.path.join(download_folder, filename), 'wb') as file:
                file.write(response.content)

            print(f"Downloaded: {filename}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    #source_url = "https://www.mtggoldfish.com/decks/budget/commander#paper"
    source_url= = "https://www.mtggoldfish.com/metagame/commander/full?page=1#paper"
    result = get_paper_urls(source_url)

    if result:
        print("Original Paper URLs:")
        for url in result:
            print(url)

        modified_urls = modify_urls(result)

        print("\nModified URLs:")
        for url in modified_urls:
            print(url)

        download_folder = "downloads"
        os.makedirs(download_folder, exist_ok=True)

        print(f"\nDownloading files to '{download_folder}':")
        download_files(modified_urls, download_folder)
