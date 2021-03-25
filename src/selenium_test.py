#!/usr/bin/env python
from selenium import webdriver
import pytest
import time
from pom.pages import (CartPage, CartModal, HomePage,
                       SearchResultsPage, SignInPage)

# URLs we are going to uuse
PRACTICE_WEBPAGE_HOME_URL = 'http://automationpractice.com/index.php'
PRACTICE_WEBPAGE_CART_CHECKOUT_URL = 'http://automationpractice.com/index.php?controller=order'

# CONSTANTS
USERNAME = 'something@something.com'
PASSWORD = 'something'

# We need this data to traverse different tests.
total_shipping_cost = 2.0 # Shipping cost is static at $2.00
cart_list = [] # List data object for tracking cart items.

class Driver(object):
    '''Context manager class for the Selenium webdriver.'''
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

@pytest.fixture(scope='session')
def browser(driver=webdriver.Chrome(),
            webpage_url=PRACTICE_WEBPAGE_HOME_URL):
    '''pytest test fixture for initializing the browser.
    Scope is "session so we don't close the driver until all test have completed." 
    
    Args:
        driver (obj): Webdriver object.
        webpage_url (str): THe webpage URL for the webdrive initialization.'''

    # Context manager for closing drivers after the tests complete.
    with Driver(driver) as driver:
        driver.get(webpage_url)
        yield driver

def test_page_loads(browser):
    '''Test to make sure the home page loads as expected.'''
    homepage = HomePage(browser)
    assert(homepage.is_title_correct)

def test_cart_is_empty_on_load(browser):
    '''Test to make sure the cart is empty on the initial home page load.'''
    homepage = HomePage(browser)
    assert(homepage.cart_quantity != 0)
    assert(homepage.cart_no_quantity)

def test_search_empty(browser):
    '''Test to make sure that not inputing a search term that the user gets
    the appropiate message.'''
    homepage = HomePage(browser)
    browser.get(PRACTICE_WEBPAGE_CART_CHECKOUT_URL)
    homepage.search_and_click('') # Empty string.
    searchpage = SearchResultsPage(browser)
    assert(searchpage.check_results_expect_empty('Please enter a search keyword'))

def test_search_known_good_search_term(browser):
    '''Test to make sure that a known search term get the correct results.'''
    homepage = HomePage(browser)
    browser.get(PRACTICE_WEBPAGE_CART_CHECKOUT_URL)
    homepage.search_and_click('Dress') # Empty string.
    searchpage = SearchResultsPage(browser)
    assert(searchpage.check_results_known_search_term('Dress'))

def test_switch_to_list_view(browser):
    '''Switch to list view and confirm the action took place.'''
    searchpage = SearchResultsPage(browser)
    searchpage.switch_check_to_list_view()

def test_switch_to_grid_view(browser):
    '''Switch to grid view and confirm the action took place.'''
    searchpage = SearchResultsPage(browser)
    searchpage.switch_check_to_grid_view()

def test_sign_on(browser):
    '''Test the sign going to the sign on page.'''
    homepage = HomePage(browser)
    browser.get(PRACTICE_WEBPAGE_HOME_URL)
    signonpage = SignInPage(browser)

    assert(signonpage.click_signin_page())

def test_user_validation(browser):
    '''Test the sign on feature with various incorrect variations.
    We'll end off on a good signon.'''
    signonpage = SignInPage(browser)
    signonpage.check_login_behavior()

def test_sign_off(browser):
    '''Test the sign going to the sign on page.'''
    signonpage = SignInPage(browser)
    assert(signonpage.click_logout())

def test_load_cart_home_page(browser):
    '''Test ordering on the main page for correctness.
    This also primes the cart page with expected items.'''
    # Initialize the home page driver and go to the home page.
    homepage = HomePage(browser)
    browser.get(PRACTICE_WEBPAGE_HOME_URL)

    # Get items from home page to test the cart feature for correctness.
    cart_items = homepage.items_list()

    # Test adding the cart items from the home page by itereating through each items.
    for num, item in enumerate(cart_items):
        (name, price) = homepage.hover_then_click_add(item)
        cart_list.append({'name': name, 'price': price, 'number_of_items': 1})
        model = CartModal(browser)

        # Calculate.
        price_total = float('{0:.2f}'.format(sum([i['price'] for i in cart_list])))
        qty_total = sum([i['number_of_items'] for i in cart_list])

        # Test contents in the modal.
        assert(model.confirm_cart_product_name(name))
        assert(model.confirm_cart_product_price(price))
        assert(model.confirm_cart_product_qty(1))
        assert(model.confirm_total_product_qty(1))
        assert(model.confirm_block_product_total(price_total))
        assert(model.confirm_shipping_cost(total_shipping_cost))
        assert(model.confirm_cart_total(total_shipping_cost+price_total))

        # Clost the modal that pops up after checking the data is correct.
        model.close_modal()

def test_load_cart_page(browser):
    '''Go to the cart page for checkout. Make sure we are in the page.'''
    cartpage = CartPage(browser)
    assert(cartpage.click_cart_page())

def test_current_cart_numbers(browser):
    '''Check to make sure the numbers in the cart are good.'''
    cartpage = CartPage(browser)
    assert(cartpage.check_cart_correctness(total_shipping_cost, cart_list))

def test_add_product_to_cart(browser):
    '''Check to make sure additional items fo a product can be added.'''
    cartpage = CartPage(browser)
    (qty, total_item_price) = cartpage.add_product_item()
    cart_list[0]['number_of_items'] += 1
    assert(qty == cart_list[0]['number_of_items'])
    assert(total_item_price == (cart_list[0]['price'] * cart_list[0]['number_of_items']))
    assert(cartpage.check_cart_correctness(total_shipping_cost, cart_list))

def test_remove_product_from_cart(browser):
    '''Check to make sure additional items fo a product can be removed.'''
    cartpage = CartPage(browser)
    (qty, total_item_price) = cartpage.delete_product_item()
    cart_list[0]['number_of_items'] -= 1
    assert(qty == cart_list[0]['number_of_items'])
    assert(total_item_price == (cart_list[0]['price'] * cart_list[0]['number_of_items']))
    cartpage.check_cart_correctness(total_shipping_cost, cart_list)

def test_remove_item_from_cart(browser):
    '''Check to make sure a product can be removed from the cart list.'''
    cartpage = CartPage(browser)
    cartpage.delete_product_item()
    del(cart_list[0])
    assert(cartpage.check_cart_correctness(total_shipping_cost, cart_list))

def test_user_must_signin_to_checkout(browser):
    '''We are signed off at this point. Let's make sure when we checkout it takes
    us to the sign on page and then the next step, to fill out address info.'''
    # We'll be visiting the sign on and cart page.
    cartpage = CartPage(browser)
    signonpage = SignInPage(browser)

    # Checkout and make sure we are in the sign in page.
    cartpage.checkout()
    assert(signonpage.check_authentication_page())

    # Fill out authentication with valid username and password then check page.
    signonpage.fillout_authenticator(USERNAME, PASSWORD)
    assert(cartpage.is_address_page())
