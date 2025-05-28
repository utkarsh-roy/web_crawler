# Simple Web Link Extractor

## Description

This Python script crawls a single webpage specified by a URL, extracts all unique hyperlinks ( `<a>` tag `href` attributes) found on that page, and outputs them in a JSON format. It attempts to mimic a standard browser by using a selection of User-Agent strings and common browser headers.

## Features

* Extracts all unique links from a given webpage.
* Converts relative URLs to absolute URLs.
* Handles basic HTTP errors and exceptions.
* Outputs results in a structured JSON format, including:
    * Requested URL
    * Final URL after redirects
    * Page Title
    * Count of unique links found
    * List of extracted links
* Includes a list of User-Agents and rotates them.
* Sends common browser headers with requests.

## Requirements

* Python 3.x
* Libraries:
    * `requests`
    * `beautifulsoup4`

## Installation

1.  **Clone the repository or download the script `link_crawler.py`.**
    (If you are not using Git, simply ensure you have `link_crawler.py`.)

2.  **Install Python 3.x** if you don't have it already.

3.  **Install the required libraries:**
    Open your terminal or command prompt, navigate to the project directory, and run:
    ```bash
    pip install -r requirements.txt
    ```
    (If you didn't create `requirements.txt`, you can install them individually: `pip install requests beautifulsoup4`)

## Usage

1.  Open your terminal or command prompt.
2.  Navigate to the directory where `link_crawler.py` is saved.
3.  Run the script using the following command:

    ```bash
    python link_crawler.py
    ```

4.  The script will prompt you to enter the website URL you wish to crawl:

    ```
    Enter the website URL to crawl:
    ```

5.  Enter the full URL (e.g., `https://example.com`) and press Enter.

6.  The script will then attempt to fetch and parse the webpage, and the extracted links will be printed to the console in JSON format.

## Output Example

If successful, the output will be a JSON object similar to this:

```json
{
    "requested_url": "[https://example.com](https://example.com)",
    "final_url_crawled": "[https://example.com/](https://example.com/)",
    "page_title": "Example Domain",
    "links_count": 1,
    "extracted_links": [
        "[https://www.iana.org/domains/example](https://www.iana.org/domains/example)"
    ]
}