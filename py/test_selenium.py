from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time
import os

# Initialize the WebDriver
#driver = webdriver.Chrome()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

WWW_PATH = "http://127.0.0.1:5000"

# Open the Flask application
driver.get(WWW_PATH)

# Interact with the page
print("/: " + driver.title)  # Print the title of the page
print(driver.page_source) # Print the HTML content of the page

# Make screenshot with exception handling
screenshot_path = "../screenshots/ss.png"
try:
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    driver.save_screenshot(screenshot_path)
    screenshot = Image.open(screenshot_path)
    screenshot.show()
except Exception as e:
    print(f"Execute test from the 'py' root directory. Error saving screenshot: {e}")

# Test the /planet_distances route
driver.get(WWW_PATH + '/planet_distances')
print("/planet_distances: " + driver.title)

# Test the /foobar route
driver.get(WWW_PATH + '/foobar')
print("/foobar: " + driver.title)

# Close the WebDriver
driver.quit()