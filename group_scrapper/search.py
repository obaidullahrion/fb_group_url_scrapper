import re
import time
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def search_groups(session, keyword, limit=50):
    """
    Search for Facebook groups based on keyword using Selenium
    
    Args:
        session: Authenticated requests session with cookies (used to transfer cookies to Selenium)
        keyword: Search keyword
        limit: Maximum number of results to return
        
    Returns:
        List of group URLs
    """
    # Format the search URL - specifically for groups
    import urllib.parse
    encoded_keyword = urllib.parse.quote(keyword)
    search_url = f"https://www.facebook.com/search/groups/?q={encoded_keyword}&epa=SEARCH_BOX"
    
    results = []
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start maximized
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    
    print("Launching browser for search...")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # First load Facebook to set cookies
        driver.get("https://www.facebook.com/")
        
        # Transfer cookies from requests session to Selenium
        for cookie in session.cookies:
            cookie_dict = {
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path
            }
            # Add secure and httpOnly if they exist
            if hasattr(cookie, 'secure') and cookie.secure:
                cookie_dict['secure'] = True
            if hasattr(cookie, 'rest') and 'HttpOnly' in cookie.rest:
                cookie_dict['httpOnly'] = True
            
            try:
                driver.add_cookie(cookie_dict)
            except Exception as e:
                print(f"Could not add cookie {cookie.name}: {e}")
        
        # Navigate to the search URL
        print(f"Navigating to: {search_url}")
        driver.get(search_url)
        
        # Wait for the page to load
        time.sleep(3)  # Initial wait for page load
        
        # Check if we're on the right page
        try:
            # Wait for groups to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@role, 'main')]//a[contains(@href, '/groups/')]")))            
            print("Groups page loaded successfully")
        except TimeoutException:
            print("Could not find group elements on the page. Facebook may have changed their layout.")
            # Save the page source for debugging
            with open("facebook_search_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page source saved to facebook_search_page.html for debugging")
            return []
        
        # Scroll to load more results
        scroll_count = 0
        max_scrolls = 10  # Limit scrolling to avoid infinite loops
        
        while len(results) < limit and scroll_count < max_scrolls:
            # Extract group links from current page
            group_links = []
            group_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/')]")
            
            for element in group_elements:
                href = element.get_attribute('href')
                if href and 'facebook.com/groups/' in href:
                    # Clean the URL (remove tracking parameters)
                    clean_url = re.sub(r'\?.*', '', href)
                    
                    # Add to results if not already present
                    if clean_url not in results and clean_url not in group_links:
                        group_links.append(clean_url)
            
            # Add new links to results
            if group_links:
                results.extend(group_links)
                print(f"Found {len(group_links)} new groups. Total: {len(results)}")
            
            # If we have enough results, break
            if len(results) >= limit:
                break
                
            # Scroll down to load more
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            scroll_count += 1
            print(f"Scrolled {scroll_count} times. Waiting for more content to load...")
            time.sleep(2)  # Wait for content to load
        
        # Limit the results to the specified limit
        return results[:limit]
    
    except Exception as e:
        print(f"Error searching for groups: {e}")
        return results[:limit] if results else []
    finally:
        # Always close the browser
        print("Closing browser...")
        driver.quit()

# Function removed as we now use Selenium directly to extract group links