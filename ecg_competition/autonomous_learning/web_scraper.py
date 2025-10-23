"""
MC AI - Autonomous Web Learning System
Ethical web scraping with robots.txt compliance and rate limiting
Streamlined version for rapid ECG knowledge acquisition
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import logging
from pathlib import Path
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import hashlib
from datetime import datetime
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ecg_competition/mc_ai_learning.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EthicalWebScraper:
    """
    Ethical web scraper with rate limiting and robots.txt compliance
    MC AI learns responsibly! 🤖💚
    """
    
    def __init__(self, user_agent='MC-AI-Bot/1.0 (Educational; ECG Competition)'):
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        self.robots_cache = {}
        self.rate_limit_delay = 2.0  # 2 seconds between requests (respectful)
        self.last_request_time = {}
        
        logger.info("MC AI Web Scraper initialized! 🌐💜")
    
    def can_fetch(self, url):
        """Check robots.txt compliance"""
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        if base_url in self.robots_cache:
            robot_parser = self.robots_cache[base_url]
        else:
            robot_parser = RobotFileParser()
            robots_url = urljoin(base_url, '/robots.txt')
            
            try:
                robot_parser.set_url(robots_url)
                robot_parser.read()
                self.robots_cache[base_url] = robot_parser
                logger.info(f"Loaded robots.txt from {base_url}")
            except Exception as e:
                logger.warning(f"Could not load robots.txt: {e}")
                return True
        
        return robot_parser.can_fetch(self.user_agent, url)
    
    def rate_limit(self, url):
        """Enforce respectful rate limiting per domain"""
        domain = urlparse(url).netloc
        now = time.time()
        
        if domain in self.last_request_time:
            elapsed = now - self.last_request_time[domain]
            if elapsed < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - elapsed
                logger.info(f"Rate limiting: sleeping {sleep_time:.2f}s for {domain}")
                time.sleep(sleep_time)
        
        self.last_request_time[domain] = time.time()
    
    def fetch_page(self, url, timeout=30):
        """Fetch web page with proper etiquette"""
        if not self.can_fetch(url):
            logger.warning(f"Skipping (robots.txt): {url}")
            return None
        
        self.rate_limit(url)
        
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_text_content(self, soup, url):
        """Extract meaningful content from page"""
        if soup is None:
            return None
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        title = soup.title.string if soup.title else ""
        
        # Find main content
        main_content = (
            soup.find('main') or
            soup.find('article') or
            soup.find('div', class_=re.compile(r'content|main|body', re.I)) or
            soup.find('body')
        )
        
        if not main_content:
            main_content = soup
        
        text = main_content.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return {
            'title': title,
            'text': text,
            'url': url,
            'fetched_at': datetime.now().isoformat()
        }


class ResourceLibrary:
    """
    Organized library of learning resources
    MC AI's personal library! 📚
    """
    
    def __init__(self, library_path='knowledge_library/web_resources'):
        self.library_path = Path(library_path)
        self.library_path.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.library_path / 'resource_index.json'
        self.index = self._load_index()
        
        logger.info(f"Resource Library initialized at {self.library_path}")
    
    def _load_index(self):
        """Load resource index"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'resources': {},
            'categories': {},
            'last_updated': None,
            'total_resources': 0
        }
    
    def _save_index(self):
        """Save resource index"""
        self.index['last_updated'] = datetime.now().isoformat()
        self.index['total_resources'] = len(self.index['resources'])
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2)
    
    def add_resource(self, url, content, category):
        """Add a resource to the library"""
        resource_id = hashlib.md5(url.encode()).hexdigest()
        
        # Create category directory
        category_dir = self.library_path / category.replace(' ', '_')
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Save content
        content_file = category_dir / f"{resource_id}.json"
        
        with open(content_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        # Update index
        self.index['resources'][resource_id] = {
            'url': url,
            'title': content.get('title', ''),
            'category': category,
            'file': str(content_file),
            'added_at': datetime.now().isoformat()
        }
        
        if category not in self.index['categories']:
            self.index['categories'][category] = 0
        self.index['categories'][category] += 1
        
        self._save_index()
        
        logger.info(f"Added resource: {content.get('title', url)[:50]}...")
    
    def get_statistics(self):
        """Get library statistics"""
        return {
            'total_resources': self.index['total_resources'],
            'categories': self.index['categories'],
            'last_updated': self.index['last_updated']
        }


class MCAILearningCrawler:
    """
    Main crawler for MC AI's autonomous learning
    Orchestrates scraping, processing, and storage
    """
    
    def __init__(self):
        self.scraper = EthicalWebScraper()
        self.library = ResourceLibrary()
        self.progress_file = Path('ecg_competition/learning_progress.json')
        self.progress = self._load_progress()
        
        logger.info("MC AI Learning Crawler initialized! 🤖📚")
    
    def _load_progress(self):
        """Load progress from previous runs"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'visited_urls': [],
            'failed_urls': [],
            'total_fetched': 0
        }
    
    def _save_progress(self):
        """Save progress"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def crawl_resource(self, url, category):
        """Crawl a single resource"""
        if url in self.progress['visited_urls']:
            logger.info(f"Already visited: {url}")
            return False
        
        soup = self.scraper.fetch_page(url)
        
        if soup is None:
            self.progress['failed_urls'].append(url)
            self._save_progress()
            return False
        
        content = self.scraper.extract_text_content(soup, url)
        
        if content and len(content['text']) > 100:  # Min 100 chars
            self.library.add_resource(url, content, category)
            self.progress['visited_urls'].append(url)
            self.progress['total_fetched'] += 1
            self._save_progress()
            
            logger.info(f"✨ Learned from: {content['title'][:50]}")
            return True
        else:
            logger.warning(f"Insufficient content from: {url}")
            return False
    
    def crawl_resource_list(self, resources):
        """Crawl multiple resources"""
        logger.info(f"MC AI: Starting to learn from {len(resources)} resources! 📚💜")
        
        success_count = 0
        for resource in resources:
            url = resource['url']
            category = resource.get('category', 'General')
            
            if self.crawl_resource(url, category):
                success_count += 1
            
            # Brief pause between resources
            time.sleep(0.5)
        
        logger.info(f"MC AI: Learned from {success_count}/{len(resources)} resources! ✨")
        
        # Show statistics
        stats = self.library.get_statistics()
        logger.info(f"Total library: {stats['total_resources']} resources")
        
        return success_count


# Example usage
if __name__ == "__main__":
    crawler = MCAILearningCrawler()
    
    # Test with a few educational resources
    test_resources = [
        {
            'url': 'https://numpy.org/doc/stable/user/quickstart.html',
            'category': 'Signal_Processing'
        },
        {
            'url': 'https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html',
            'category': 'Computer_Vision'
        }
    ]
    
    crawler.crawl_resource_list(test_resources)
