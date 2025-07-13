from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import os

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
# Removed headless mode for debugging
chrome_options.add_argument('--start-maximized')  # Maximize the browser window

# Path to ChromeDriver
CHROME_DRIVER_PATH = r"K:\Setup\chromedriver.exe"

def initialize_driver():
    service = Service(CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

def random_sleep(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def handle_popup(driver):
    try:
        # Wait for the popup to appear and find the close button
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Close']"))
        )
        close_button.click()
        print("Popup closed successfully")
    except TimeoutException:
        print("No popup found or unable to close popup")
    except Exception as e:
        print(f"Error handling popup: {str(e)}")

def get_subscriber_count(driver):
    try:
        # Wait for the subscriber count element to be visible
        subscriber_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'x193iq5w')]//a[contains(@href, '/followers/')]"))
        )
        return subscriber_element.text.split()[0]  # Extract the number
    except TimeoutException:
        print("Couldn't find subscriber count")
        return "N/A"
    except Exception as e:
        print(f"Error getting subscriber count: {str(e)}")
        return "Error"

def extract_page_info(driver, username):
    url = f"https://www.facebook.com/{username}"
    
    try:
        print(f"Navigating to {url}")
        driver.get(url)
        random_sleep()
        
        print("Checking for popup")
        handle_popup(driver)
        random_sleep()
        
        print("Attempting to get subscriber count")
        subscriber_count = get_subscriber_count(driver)
        print(f"Username: {username}")
        print(f"Subscriber Count: {subscriber_count}")
        print("-" * 30)
    except Exception as e:
        print(f"Error extracting info for {username}: {str(e)}")
        print("-" * 30)

def main():
    driver = initialize_driver()
    
    try:
        # List of Facebook page usernames
        usernames = [
            "MetaAI",
            "Google",
            "Amazon",
            "Microsoft"
        ]
        
        print("Facebook Page Subscriber Counts:")
        print("=" * 30)
        
        for username in usernames:
            extract_page_info(driver, username)
            random_sleep(5, 10)  # Longer sleep between pages
    
    except Exception as e:
        print(f"An error occurred in main: {str(e)}")
    
    finally:
        input("Press Enter to close the browser...")
        driver.quit()

if __name__ == "__main__":
    main()