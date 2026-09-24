import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    download_path = os.path.abspath("downloads")

    options = Options()

    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    yield driver

    driver.quit()


def test_homepage_loaded(driver):

    driver.get("https://bstackdemo.com/")

    assert "bstackdemo" in driver.current_url.lower()

    print("BrowserStack Demo home page loaded successfully")


def test_select_product(driver):

    driver.get("https://bstackdemo.com/")

    # Select iPhone 12
    product = driver.find_element(By.ID, "1")

    print("iPhone 12 product selected")

    # Add to cart
    add_to_cart = product.find_element(
        By.CLASS_NAME,
        "shelf-item__buy-btn"
    )

    add_to_cart.click()

    print("Product added to cart successfully")
    time.sleep(1)

    # Wait for cart product name
    wait = WebDriverWait(driver, 10)

    cart_product = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".shelf-item__details .title")
        )
    )

    assert cart_product.text == "iPhone 12"

    print("iPhone 12 is present in the cart")

    # Verify quantity
    cart_details = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".shelf-item__details .desc")
        )
    )

    assert "Quantity: 1" in cart_details.text

    print("iPhone 12 with quantity 1 is present in the cart")

    checkout = driver.find_element(
        By.CLASS_NAME,
        "buy-btn"
    )

    checkout.click()

    print("Checkout button clicked successfully")

    # Select Username
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, "username")
        )
    )

    username.click()

    print("Username field selected")

    # Wait for the dropdown option
    username_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "(//*[contains(@id, 'react-select-') and contains(@id, '-option-')])[1]")
        )
    )

    username_option.click()
    print("First username option selected")
    time.sleep(2)

    # Select Password
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "password"))
    )

    password.click()

    print("Password field clicked")

    # Select first password option
    password_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "(//*[contains(@id, 'react-select-') and contains(@id, '-option-')])[1]")
        )
    )

    password_option.click()

    print("First password option selected")
    time.sleep(2)

    # Click Login
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    )

    login_button.click()

    print("Login button clicked successfully")

    # Verify Shipping Address page
    shipping_heading = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='shipping-address-heading']")
        )
    )

    assert shipping_heading.text == "Shipping Address"

    print("Shipping Address page loaded successfully")

    # First Name
    first_name = driver.find_element(By.ID, "firstNameInput")
    first_name.send_keys("John")

    print("First Name entered")
    time.sleep(2)

    # Last Name
    last_name = driver.find_element(By.ID, "lastNameInput")
    last_name.send_keys("Doe")

    print("Last Name entered")
    time.sleep(2)

    # Address
    address = driver.find_element(By.ID, "addressLine1Input")
    address.send_keys("123 Main Street")

    print("Address entered")
    time.sleep(2)

    # State / Province
    province = driver.find_element(By.ID, "provinceInput")
    province.send_keys("California")

    print("State/Province entered")
    time.sleep(2)

    # Postal Code
    postal_code = driver.find_element(By.ID, "postCodeInput")
    postal_code.send_keys("90001")

    print("Postal Code entered")
    time.sleep(2)

    # Submit
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, "checkout-shipping-continue")
        )
    )

    submit_button.click()

    print("Shipping address submitted successfully")

    # Verify order confirmation
    confirmation = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "confirmation-message")
        )
    )

    assert confirmation.text == "Your Order has been successfully placed."

    print("Order placed successfully")

    # Verify order number
    order_text = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Your order number is')]")
        )
    )

    assert "Your order number is" in order_text.text

    print("Order confirmation verified successfully")
    time.sleep(2)

    # Download order receipt
    download_receipt = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "downloadpdf")
        )
    )

    download_receipt.click()

    print("Download receipt clicked successfully")

    # Verify confirmation.pdf is downloaded
    download_path = os.path.abspath("downloads")
    pdf_file = os.path.join(download_path, "confirmation.pdf")

    wait.until(
        lambda driver: os.path.exists(pdf_file)
    )

    print("confirmation.pdf downloaded successfully")

    assert os.path.exists(pdf_file)

    print("Order receipt download verified successfully")
    time.sleep(1)

    # Continue Shopping
    continue_shopping = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Continue Shopping')]")
        )
    )

    continue_shopping.click()

    print("Continue Shopping clicked successfully")
    time.sleep(1)

    wait.until(
        EC.url_to_be("https://bstackdemo.com/")
    )

    print("Returned to shopping page successfully")
    time.sleep(2)
