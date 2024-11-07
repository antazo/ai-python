#!/usr/bin/env python3
# testweb.py

# TODO: Comment out and implement the test results when the endpoints are up
# HINT: Check for the Azure AI APIs documentation
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (e.g., ChromeDriver)
driver = webdriver.Chrome()

# Define the base URL of your application
base_url = "http://127.0.0.1"

# Test the home page
def test_home_page():
    driver.get(base_url)
    assert "Home" in driver.title
    print("Home page test passed.")

# Test the translator page
def test_translator_page():
    driver.get(base_url + "/translator")
    assert "Translator" in driver.title

    # Find the form elements
    text_input = driver.find_element(By.NAME, "text")
    language_input = driver.find_element(By.NAME, "language")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    # Fill out the form and submit
    #text_input.send_keys("Hello")
    #language_input.send_keys("es")
    #submit_button.click()

    # Wait for the result
    #time.sleep(3)

    # Verify the result
    #result = driver.find_element(By.ID, "translated_text")
    #assert "Hola" in result.text
    print("Translator page test passed.")

# Test the vision page
def test_vision_page():
    driver.get(base_url + "/vision")
    assert "Vision" in driver.title

    # Find the form elements
    file_input = driver.find_element(By.ID, "image")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    # Upload an image and submit
    #file_input.send_keys("uploads/sample.png")
    #submit_button.click()

    # Wait for the result
    #time.sleep(3)

    # Verify the result
    #result = driver.find_element(By.ID, "description-container")
    #assert "Description" in result.text
    print("Vision page test passed.")

# Run the tests
if __name__ == "__main__":
    try:
        test_home_page()
        test_translator_page()
        test_vision_page()
    finally:
        driver.quit()