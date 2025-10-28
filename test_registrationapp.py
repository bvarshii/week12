import pytest
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import app

@pytest.fixture(scope="module")
def setup_teardown():
    # Start Flask app in background thread
    flask_thread = threading.Thread(target=lambda: app.run(port=5000))
    flask_thread.daemon = True
    flask_thread.start()
    time.sleep(2)

    driver = webdriver.Chrome()
    yield driver

    driver.quit()

def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").send_keys("secret123")
    driver.find_element(By.ID, "submit").click()
    time.sleep(1)
    assert "Username is required" in driver.page_source

def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("John")
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.ID, "submit").click()
    time.sleep(1)
    assert "Password is required" in driver.page_source

def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.ID, "submit").click()
    time.sleep(1)
    assert "Password too short" in driver.page_source

def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Alice")
    driver.find_element(By.NAME, "password").send_keys("goodpassword")
    driver.find_element(By.ID, "submit").click()
    time.sleep(1)
    assert "Registration successful" in driver.page_source
