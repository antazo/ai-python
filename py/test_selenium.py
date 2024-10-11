from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the Flask application
driver.get('http://127.0.0.1:8888/')

# Interact with the page
print("/: " + driver.title)  # Print the title of the page
print(driver.page_source) # Print the HTML content of the page
driver.save_screenshot("../screenshots/ss.png") # Make screenshot
screenshot = Image.open("../screenshots/ss.png")
screenshot.show()

# Test the /planet_distances route
driver.get('http://127.0.0.1:8888/planet_distances')
print("/planet_distances: " + driver.title)

# Test the /foobar route
driver.get('http://127.0.0.1:8888/foobar')
print("/foobar: " + driver.title)

# Close the WebDriver
driver.quit()