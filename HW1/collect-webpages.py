import requests
from bs4 import BeautifulSoup
import time
import sys
import random
from urllib.parse import urljoin

# Function to check if the URL is an HTML page with more than 1000 bytes
def is_valid_html(url):
    try:
        response = requests.get(url, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        content_length = int(response.headers.get('Content-Length', 0))
        
        if 'text/html' in content_type and content_length > 1000:
            return response.url
        else:
            return None
    except requests.RequestException:
        return None

# Function to extract all links from a given webpage URL
def extract_links(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()  # Use set to avoid duplicate links

        for anchor in soup.find_all('a', href=True):
            link = anchor['href']
            full_link = urljoin(url, link)  # Join with base URL if needed
            links.add(full_link)

        return links
    except requests.RequestException:
        return set()

# Main function
def collect_webpages(seed_url, target_count=500):
    collected_uris = set()
    to_process = {seed_url}

    while len(collected_uris) < target_count:
        print(f"Need to collect {target_count - len(collected_uris)} more URIs...")

        # Pick a random seed URL from the to_process set
        current_url = random.choice(list(to_process))
        print(f"Random seed: {current_url}")

        # Extract links from the current URL
        links = extract_links(current_url)

        # Check each link to see if it is a valid HTML page with more than 1000 bytes
        for link in links:
            if len(collected_uris) >= target_count:
                break

            valid_url = is_valid_html(link)
            if valid_url and valid_url not in collected_uris:
                collected_uris.add(valid_url)
                to_process.add(valid_url)

        time.sleep(1)  # Add a delay between requests to avoid overwhelming the server

    # Save the collected URIs to a file
    with open('collected_uris.txt', 'w') as file:
        for uri in collected_uris:
            file.write(uri + '\n')

    print(f"Collected {len(collected_uris)} unique URIs")
    return collected_uris

# Entry point of the script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 collect-webpages.py <seed_url>")
        sys.exit(1)

    seed_url = sys.argv[1]
    collected_uris = collect_webpages(seed_url)
    print("\nCollected URIs:")
    for uri in collected_uris:
        print(uri)
