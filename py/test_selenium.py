from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the Flask application
driver.get('http://127.0.0.1:8888/')

# Interact with the page
print(driver.title)  # Print the title of the page

# Test the /planet_distances route
driver.get('http://127.0.0.1:8888/planet_distances')
print(driver.page_source)  # Print the HTML content of the page

# Test the /sum_distances route
driver.get('http://127.0.0.1:8888/foobar')
print(driver.page_source)  # Print the HTML content of the page

# Close the WebDriver
driver.quit()