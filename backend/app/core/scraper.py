import trafilatura
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Optional
import time

class PydanticDocScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})

    def discover_urls(self) -> List[str]:
        """Discover all documentation URLs from the base URL."""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set()
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Skip external links and anchors
                if href.startswith('http') and urlparse(href).netloc != urlparse(self.base_url).netloc:
                    continue
                if href.startswith('#'):
                    continue
                # Make absolute URL
                url = urljoin(self.base_url, href)
                # Only include URLs that are under the base path
                if url.startswith(self.base_url):
                    links.add(url)
            return list(links)
        except Exception as e:
            print(f"Error discovering URLs: {e}")
            return []

    def scrape_page(self, url: str) -> Optional[Dict]:
        """Scrape a single page and return the extracted content."""
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                return None
            result = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=True,
                output_format="json",
                with_metadata=True
            )
            if result:
                return {
                    "url": url,
                    "title": result.get("title"),
                    "text": result.get("text"),
                    "author": result.get("author"),
                    "date": result.get("date")
                }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        return None

    def scrape_all(self) -> List[Dict]:
        """Scrape all discovered documentation pages."""
        urls = self.discover_urls()
        documents = []
        for url in urls:
            doc = self.scrape_page(url)
            if doc:
                documents.append(doc)
            time.sleep(0.5)  # Be polite to the server
        return documents


if __name__ == "__main__":
    # Simple test of the scraper
    scraper = PydanticDocScraper("https://docs.pydantic.dev/2.10/")
    
    print("Testing URL discovery...")
    urls = scraper.discover_urls()
    print(f"Found {len(urls)} URLs")
    print("First 5 URLs:")
    for url in urls[:5]:
        print(f"  {url}")
    
    print("\nTesting page scraping...")
    if urls:
        test_url = urls[0]
        print(f"Scraping: {test_url}")
        doc = scraper.scrape_page(test_url)
        if doc:
            print(f"Title: {doc.get('title', 'No title')}")
            print(f"Text length: {len(doc.get('text', ''))}")
        else:
            print("Failed to scrape page")
    
    print("\nTest complete!")