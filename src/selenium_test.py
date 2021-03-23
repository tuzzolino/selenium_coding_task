#!/usr/bin/env python
from selenium import webdriver
import pytest
import time
from pom.pages import (CartPage, CartModal, HomePage, SearchResultsPage)

PRACTICE_WEBPAGE_HOME_URL = 'http://automationpractice.com/index.php'
PRACTICE_WEBPAGE_CART_CHECKOUT_URL = 'http://automationpractice.com/index.php?controller=order'

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

@pytest.fixture(scope="session")
def browser(driver=webdriver.Chrome(),
            webpage_url=PRACTICE_WEBPAGE_HOME_URL):
    '''pytest test fixture for initializing the browser.
    
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

def test_main_page_cart(browser):
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
        model.close_modal()

def test_cart(browser):
    browser.get(PRACTICE_WEBPAGE_CART_CHECKOUT_URL)
    cartpage = CartPage(browser)

def test_user_must_signin_to_checkout(browser):
    pass
    # self.homePage.search()
    # self.searchResultsPage=SearchResultsPage(self.homePage.driver)
    # self.searchResultsPage.click_search_result()
    # self.searchResultsPage.driver.switch_to_window(self.searchResultsPage.driver.window_handles[1])
    # self.productDetailsPage=ProductDetailsPage(self.searchResultsPage.driver)
    # self.productDetailsPage.click_add_to_cart_button()
    # self.subCartPage=SubCartPage(self.productDetailsPage.driver)
    # self.subCartPage.click_cart_link()
    # # instantiate an object of Cart Page class
    # self.cartPage=CartPage(self.subCartPage.driver)    
    # #click on Proceed to Checkout button
    # self.cartPage.click_proceed_to_checkout_button()
    # # instantiate an object of SignIn Page class
    # self.signInPage=SignInPage(self.cartPage.driver)
    # # to assert we are in indeed on Sign In Page, first we assert the title of the page
    # self.assertTrue(TestData.SIGN_IN_PAGE_TITLE,self.signInPage.driver.title)
    # # and then we assert for presence of email textbox on the page
    # self.assertTrue(self.signInPage.is_visible(Locators.USER_EMAIL_OR_MOBIL_NO_TEXTBOX))