import os
import pickle
import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests

# Constants
COOKIE_FILE = "facebook_cookies.pkl"
LOGIN_URL = "https://www.facebook.com/login.php"

def authenticate():
    """
    Authenticate with Facebook using Selenium and save cookies to a file
    """
    print("Facebook Login")
    email = input("Email: ")
    password = getpass("Password: ")
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start maximized
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    
    # Uncomment the line below if you want to run Chrome in headless mode
    # chrome_options.add_argument("--headless")
    
    print("Launching browser...")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to Facebook login page
        driver.get("https://www.facebook.com/")
        print("Navigating to Facebook login page...")
        
        # Wait for the cookie policy dialog and accept it if present
        try:
            cookie_accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Allow') or contains(text(), 'Accept') or contains(text(), 'OK')]")))            
            cookie_accept_button.click()
            print("Accepted cookies policy")
        except TimeoutException:
            print("No cookie policy dialog found or already accepted")
        
        # Wait for email field and enter credentials
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email")))
        email_field.clear()
        email_field.send_keys(email)
        
        password_field = driver.find_element(By.ID, "pass")
        password_field.clear()
        password_field.send_keys(password)
        
        # Click login button
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        
        # Wait for login to complete - check for common elements on the Facebook homepage
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='navigation']" + 
                                              " | //div[@data-pagelet='Stories']" + 
                                              " | //div[contains(@aria-label, 'Facebook')]" +
                                              " | //div[@aria-label='Create']")))
            print("Login successful!")
        except TimeoutException:
            print("Login might have failed or additional verification might be required.")
            print("Please complete any additional steps in the browser window.")
            
            # Wait for manual intervention if needed
            input("Press Enter after completing any additional verification steps...")
        
        # Create a requests session and add the selenium cookies to it
        session = requests.Session()
        
        # Set a user agent to mimic the browser
        headers = {
            "User-Agent": driver.execute_script("return navigator.userAgent;")
        }
        session.headers.update(headers)
        
        # Transfer cookies from Selenium to requests session
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
        
        # Save cookies to file
        save_cookies(session)
        return session
        
    finally:
        # Close the browser
        print("Closing browser...")
        driver.quit()

def save_cookies(session):
    """
    Save session cookies to a file
    """
    with open(COOKIE_FILE, 'wb') as f:
        pickle.dump(session.cookies, f)
    print(f"Cookies saved to {COOKIE_FILE}")

def load_cookies():
    """
    Load cookies from file and return a new session
    """
    if not os.path.exists(COOKIE_FILE):
        print(f"Cookie file {COOKIE_FILE} not found")
        return None
    
    session = requests.Session()
    
    # Set a user agent to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    session.headers.update(headers)
    
    # Load cookies
    with open(COOKIE_FILE, 'rb') as f:
        session.cookies.update(pickle.load(f))
    
    return session