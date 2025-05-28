import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import random # For selecting a random User-Agent

# List of some common User-Agent strings
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

def get_all_website_links(url):
    """
    Crawls a single webpage and extracts all unique absolute links.
    Attempts to mimic a browser request more closely.

    Args:
        url (str): The URL of the webpage to crawl.

    Returns:
        str: A JSON string containing a list of unique absolute URLs found on the page,
             or a JSON string with an error message if crawling fails.
    """
    found_links = set()
    error_message = None
    page_title = "N/A"
    final_url_after_redirects = url # Initialize with requested URL

    try:
        # Select a random User-Agent
        user_agent = random.choice(USER_AGENTS)
        
        # Common browser headers
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br', # requests handles gzip/deflate automatically
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1', # Do Not Track
        }
        
        # Create a session object to persist parameters like headers
        session = requests.Session()
        session.headers.update(headers)

        # Make the request using the session
        response = session.get(url, timeout=15, allow_redirects=True) # Increased timeout slightly
        final_url_after_redirects = response.url # Get the final URL after any redirects
        
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        soup = BeautifulSoup(response.content, "html.parser")

        if soup.title and soup.title.string:
            page_title = soup.title.string.strip()

        parsed_base_url = urlparse(final_url_after_redirects)

        for a_tag in soup.find_all("a", href=True):
            href = a_tag.attrs.get("href")
            if not href: # Handles empty strings or None
                continue

            absolute_link = urljoin(final_url_after_redirects, href)
            parsed_link = urlparse(absolute_link)
            absolute_link_no_fragment = parsed_link._replace(fragment="").geturl()

            if parsed_link.scheme in ["http", "https"]:
                found_links.add(absolute_link_no_fragment)

    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP error occurred: {e} (URL: {final_url_after_redirects})"
        print(f"Error fetching {url}: {e}")
    except requests.exceptions.ConnectionError as e:
        error_message = f"Connection error occurred: {e}"
        print(f"Error connecting to {url}: {e}")
    except requests.exceptions.Timeout as e:
        error_message = f"Timeout occurred while fetching {url}: {e}"
        print(f"Timeout for {url}: {e}")
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred during request: {e}"
        print(f"Error during requests to {url}: {e}")
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(f"An unexpected error occurred: {e}")

    if error_message:
        return json.dumps({"error": error_message, "requested_url": url, "final_url_attempted": final_url_after_redirects}, indent=4)
    else:
        return json.dumps({
            "requested_url": url,
            "final_url_crawled": final_url_after_redirects,
            "page_title": page_title,
            "links_count": len(found_links),
            "extracted_links": sorted(list(found_links))
        }, indent=4)

if __name__ == "__main__":
    target_url = input("Enter the website URL to crawl: ")

    if not (target_url.startswith('http://') or target_url.startswith('https://')):
        print(f"No scheme (http/https) provided. Assuming https:// for {target_url}")
        target_url = "https://" + target_url
        
    print(f"\nCrawling {target_url} for links...\n")
    links_json_output = get_all_website_links(target_url)
    print(links_json_output)
