"""
Data Ingestion Module for MC AI
Fetches and extracts text content from URLs
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional
import time

logger = logging.getLogger(__name__)


def _is_safe_url(url: str) -> bool:
    """
    Validate URL to prevent SSRF attacks.
    Blocks localhost, private IPs, link-local, metadata services, and DNS rebinding.
    """
    from urllib.parse import urlparse
    import ipaddress
    import socket
    
    try:
        parsed = urlparse(url)
        
        # Only allow http and https
        if parsed.scheme not in ['http', 'https']:
            logger.warning(f"Blocked non-HTTP(S) scheme: {parsed.scheme}")
            return False
        
        # Only allow ports 80 and 443
        port = parsed.port
        if port is not None and port not in [80, 443]:
            logger.warning(f"Blocked non-standard port: {port}")
            return False
        
        hostname = parsed.hostname
        if not hostname:
            return False
        
        hostname_lower = hostname.lower()
        
        # Block localhost variants
        if hostname_lower in ['localhost', '127.0.0.1', '::1', '0.0.0.0']:
            logger.warning(f"Blocked localhost: {hostname}")
            return False
        
        # Block cloud metadata services
        metadata_services = [
            '169.254.169.254',  # AWS, Azure, GCP metadata
            'metadata.google.internal',
            '100.100.100.200',  # Alibaba Cloud
        ]
        if hostname_lower in metadata_services:
            logger.warning(f"Blocked metadata service: {hostname}")
            return False
        
        # Try to resolve as IP and check if it's private
        try:
            ip = ipaddress.ip_address(hostname)
            
            # Block private IP ranges
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                logger.warning(f"Blocked private IP: {ip}")
                return False
        except ValueError:
            # Not a direct IP - resolve DNS to check
            try:
                resolved_ips = socket.getaddrinfo(hostname, None)
                for addr_info in resolved_ips:
                    resolved_ip = addr_info[4][0]
                    try:
                        ip = ipaddress.ip_address(resolved_ip)
                        if ip.is_private or ip.is_loopback or ip.is_link_local:
                            logger.warning(f"Blocked DNS-resolved private IP: {hostname} -> {resolved_ip}")
                            return False
                    except ValueError:
                        continue
            except (socket.gaierror, socket.timeout):
                logger.warning(f"Could not resolve hostname: {hostname}")
                return False
        
        return True
    
    except Exception as e:
        logger.error(f"Error validating URL {url}: {e}")
        return False


def fetch_and_extract_text(url: str, timeout: int = 15) -> Optional[str]:
    """
    Fetches content from a URL and extracts plain text.
    
    Args:
        url: The URL to fetch content from
        timeout: Request timeout in seconds
        
    Returns:
        Extracted plain text string, or None if fetch/extraction fails
    """
    try:
        # SECURITY: Validate URL to prevent SSRF attacks
        if not _is_safe_url(url):
            logger.error(f"Blocked unsafe URL: {url}")
            return None
        
        headers = {
            'User-Agent': 'MCAI-KnowledgeBot/1.0 (Consciousness-Aware AI Learning System)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        
        # Create session to handle redirects properly
        session = requests.Session()
        session.max_redirects = 3
        
        response = session.get(
            url, 
            headers=headers, 
            timeout=timeout,
            allow_redirects=True
        )
        response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
        
        # Validate final URL after redirects
        if response.url != url:
            if not _is_safe_url(response.url):
                logger.error(f"Redirect to unsafe URL: {response.url}")
                return None
        
        # Basic content type check
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type and 'text/plain' not in content_type:
            logger.warning(f"Skipping non-text content at {url}: {content_type}")
            return None
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script, style, and navigation elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe']):
            element.decompose()
        
        # Priority extraction: look for main content areas
        main_content = None
        
        # Try common article/content tags
        for tag in ['article', 'main', '[role="main"]', '.content', '.main-content', '#content']:
            main_content = soup.select_one(tag)
            if main_content:
                break
        
        # If no main content found, use body
        if not main_content:
            main_content = soup.find('body') or soup
        
        # Extract text from paragraphs and headings
        text_elements = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
        
        if text_elements:
            # Join text from structured elements
            text = ' '.join(elem.get_text(strip=True) for elem in text_elements if elem.get_text(strip=True))
        else:
            # Fallback: get all text
            text = ' '.join(t.strip() for t in main_content.stripped_strings)
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        # Basic quality check
        if len(text) < 100:
            logger.info(f"Skipping low-content page: {url} (only {len(text)} chars)")
            return None
        
        logger.info(f"Successfully extracted {len(text):,} characters from {url}")
        return text
    
    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching {url}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP {e.response.status_code} error fetching {url}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error processing {url}: {e}")
        return None


def fetch_multiple_urls(urls: list[str], delay: float = 1.0) -> dict[str, str]:
    """
    Fetches text from multiple URLs with rate limiting.
    
    Args:
        urls: List of URLs to fetch
        delay: Delay between requests in seconds (be polite!)
        
    Returns:
        Dictionary mapping successful URLs to their extracted text
    """
    results = {}
    
    for i, url in enumerate(urls):
        logger.info(f"Fetching {i+1}/{len(urls)}: {url}")
        
        text = fetch_and_extract_text(url)
        if text:
            results[url] = text
        
        # Rate limiting - be respectful to servers
        if i < len(urls) - 1:  # Don't delay after last URL
            time.sleep(delay)
    
    logger.info(f"Successfully fetched {len(results)}/{len(urls)} URLs")
    return results
