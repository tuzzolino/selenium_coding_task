import random
import re
import time
import yaml

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pom.element import BasePageElement
from pom.locators import (CartPageLocator,
                          MainPageLocators,
                          SearchResultsPageLocators,
                          SignInOutLocator)

LOGIN_DATA_PATH = r'./data/logins.yml'

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def click(self, *locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).click()

    def visible(self, *locator):
        '''Wait for a locator to become visible after an interaction is performed.'''
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return bool(element)

    def disappear(self, *locator):
        '''Expect an element to not be there or to disappear. Wait 1 second.'''
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            return True
        else:
            return False

    def enter_text(self, *locator, text):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def clear_text(self, *locator, text):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).clear()

    def hover(self, *locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        ActionChains(self.driver).move_to_element(element).perform()

    def list_of_items(self, *locator, text):
        return self.driver.find_element(*locator).find_elements_by_tag_name(text)

    def wait_element(self, *locator):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print("\n * ELEMENT NOT FOUND WITHIN GIVEN TIME! --> %s" %(locator[1]))
            self.driver.quit()


class HomePage(BasePage):
    """Home page action methods are ."""
    def is_title_correct(self):
        '''Is the title of the home page correct.'''
        return bool(self.driver.find_element(*MainPageLocators.TITLE) == 'My Store')

    def items_list(self):
        '''Get a list of items from the home page.'''
        assert(self.visible(*MainPageLocators.CART_ITEMS))
        return self.list_of_items(*MainPageLocators.CART_ITEMS, text='li')

    def cart_quantity(self):
        '''Gets the scalar number of the number of items in a cart.'''
        return int(self.driver.find_element(*MainPageLocators.CART_QUANTITY).get_value())

    def cart_no_quantity(self):
        '''Get the value from the cart if it is expected to be empty.'''
        return bool(True if self.driver.find_element(*MainPageLocators.CART_NO_QUANTITY).get_value() == "(empty)" else False)

    def search_and_click(self, text):
        '''Search and click results.
        
        Args:
            text (str): Search text.'''
        self.driver.find_element(*MainPageLocators.SEARCH_TEXTBOX).clear()
        self.enter_text(*MainPageLocators.SEARCH_TEXTBOX, text=text)
        self.click(*MainPageLocators.SEARCH_SUBMIT)

    def hover_then_click_add(self, add_cart_element):
        '''Hover then click on "Add to cart".
        
        Args:
            locator (obj): cart locator item to hover and click on.
            
        Returns: tuple (item(str), price(float))'''
        # Get the hover hover object.
        hover = ActionChains(self.driver).move_to_element(add_cart_element)
        hover.perform()

        # Wait for the button item to appear and get values.
        add_cart_btn = add_cart_element.find_element(*MainPageLocators.ADD_ITEM_BTN)
        self.wait_element(*MainPageLocators.ADD_ITEM_BTN)
        item_price = add_cart_element.find_element(*MainPageLocators.ITEM_PRICE).text
        item_name = add_cart_element.find_element(*MainPageLocators.ITEM_NAME).get_attribute('title')

        # Since there are discounts let's only get the first price.
        re_obj = re.compile(r'^\$(?P<act_price>\d+\.\d{2}).*')
        assert(re_obj is not None)
        actual_price = re_obj.match(item_price)

        # Move then click on the item add.
        hover.move_to_element(add_cart_btn)

        # TODO: Randomize the clicks to get more items.
        add_cart_btn.click()

        # Wait for modal and get element
        assert(self.visible(*MainPageLocators.MODAL_CONFIRM))

        return (item_name, float(actual_price.group('act_price')))
        

class CartModal(BasePage):
    '''Methods for the modal cart items go here.'''

    def __init__(self, driver):
        self.modal = driver.find_element(*MainPageLocators.MODAL_CONFIRM)  

    def confirm_cart_product_name(self, cart_prod_name):
        '''Confirms cart product name.'''
        return bool(cart_prod_name == self.modal.find_element(*MainPageLocators.CART_PROD_NAME).text)

    def confirm_cart_product_price(self, cart_prod_price):
        '''Confirms cart product price.'''
        return bool(cart_prod_price == float(self.modal.find_element(*MainPageLocators.CART_PROD_PRICE).text.replace('$', '')))

    def confirm_cart_product_qty(self, cart_prod_qty):
        '''Confirms cart product qty.'''
        return bool(cart_prod_qty == int(self.modal.find_element(*MainPageLocators.CART_PROD_QTY).text))

    def confirm_total_product_qty(self, total_prod_qty):
        '''Confirms total product qty.'''
        return bool(total_prod_qty == int(self.modal.find_element(*MainPageLocators.TOTAL_QTY).text))

    def confirm_block_product_total(self, block_prod_price):
        '''Confirms block product total.'''
        return bool(block_prod_price == float(self.modal.find_element(*MainPageLocators.BLOCK_PROD_TOTAL).text.replace('$', '')))

    def confirm_shipping_cost(self, shipping_cost):
        '''Confirms block product total.'''
        return bool(shipping_cost == float(self.modal.find_element(*MainPageLocators.SHIPPING_COST).text.replace('$', '')))

    def confirm_cart_total(self, cart_total):
        return bool(cart_total == float(self.modal.find_element(*MainPageLocators.CART_TOTAL).text.replace('$', '')))

    def close_modal(self):
        '''Closes the modal. Randomize which button is clicked'''
        close_btn = self.modal.find_element(*MainPageLocators.CLOSE_MODAL)
        cont_btn = self.modal.find_element(*MainPageLocators.CONT_SHOPPING)
        close_btn.click() if bool(random.getrandbits(1)) else cont_btn.click()

    
class SearchResultsPage(BasePage):
    """Search results page class."""
        
    def check_results_expect_empty(self, compare_text):
        '''Check the results from an expected empty result.
        Args:
            compare_text (str): text to compare to the value of the result.'''
        assert(self.visible(*SearchResultsPageLocators.SEARCH_ALERT))
        return bool(self.driver.find_element(*SearchResultsPageLocators.SEARCH_ALERT).text == compare_text)

    def check_results_known_search_term(self, compare_text):
        '''Check the results from an expected empty result.
        Args:
            compare_text (str): text to compare to the value of the result.'''
        assert(self.visible(*SearchResultsPageLocators.CENTER_COLUMN))
        list_of_items = self.list_of_items(*SearchResultsPageLocators.LIST_OF_SEARCH_ITEMS, text='li')
        for search_item in list_of_items:
            if compare_text.lower() in search_item.text.lower():
                return False
        return True

    def switch_check_to_grid_view(self):
        '''Switch to grid view.'''
        self.click(*SearchResultsPageLocators.GRID_VIEW)
        # check for the row div to disappear or it's absence.
        return self.disappear(*SearchResultsPageLocators.ROW_VIEW)

    def switch_check_to_list_view(self):
        '''Switch to list view.'''
        self.click(*SearchResultsPageLocators.LIST_VIEW)
        # check for the row div to appear.
        return self.visible(*SearchResultsPageLocators.ROW_VIEW)


class SignInPage(BasePage):
    """Sign in Page. Test Class"""

    def click_signin_page(self):
        '''Go to the sign in page and check for authentication element div.'''
        self.hover(*MainPageLocators.SIGN_IN)
        self.click(*MainPageLocators.SIGN_IN)
        return self.check_authentication_page()

    def click_logout(self):
        '''Go to the sign in page and check for authnetication element div.'''
        self.hover(*SignInOutLocator.LOGOUT_BTN)
        self.click(*SignInOutLocator.LOGOUT_BTN)
        return self.check_authentication_page()

    def check_authentication_page(self):
        '''Are we in the authentication page?'''
        return self.visible(*SignInOutLocator.AUTHENTICATION)

    def fillout_authenticator(self, username, password):
        '''Fill out the authenticator.'''
        # First clear out input.
        self.clear_text(*SignInOutLocator.EMAIL_INPUT, text='')
        self.clear_text(*SignInOutLocator.PASSWORD_INPUT, text='')

        # Now fill out input boxes and sign in... or try.
        self.enter_text(*SignInOutLocator.EMAIL_INPUT, text=username)
        self.enter_text(*SignInOutLocator.PASSWORD_INPUT, text=password)
        self.hover(*SignInOutLocator.SUBMIT_BTN)
        self.click(*SignInOutLocator.SUBMIT_BTN)

    def check_login_behavior(self):
        '''Read from a YAML file to get test data and conditions for testing login.'''
        with open(LOGIN_DATA_PATH, 'r') as file:
            userlist = yaml.load(file, Loader=yaml.FullLoader)
            for num, item in enumerate(userlist['logins']):
                print ('Test Case: {}, Description: {}'.format(num, item['use_case']))
                self.fillout_authenticator(item['username'], item['password'])

                # We handle the passing test case differently.
                if 'My account' != item['expect']:
                    assert(self.visible(*SignInOutLocator.ALERT_TEXT))
                    assert(item['expect'] == self.driver.find_element(*SignInOutLocator.ALERT_TEXT).text)
                else:
                    assert(self.visible(*SignInOutLocator.LOGGED_IN_TEXT))
                    assert(item['expect'] == self.driver.find_element(*SignInOutLocator.LOGGED_IN_TEXT).text)

class CartPage(BasePage):
    """Search cart page action methods defined here."""

    def click_cart_page(self):
        '''Go to the sign in page and check for authnetication element div.'''
        self.hover(*MainPageLocators.CART_PAGE)
        self.click(*MainPageLocators.CART_PAGE)
        return bool(self.visible(*CartPageLocator.CART_TABLE))

    def check_cart_correctness(self, shipping_price, cart_items):
        '''Check the cart items for correctness in the cart page.'''
        total_product = float('{0:.2f}'.format(sum([i['price']*i['number_of_items'] for i in cart_items])))
        grand_total = total_product + shipping_price
        return(total_product == float(self.driver.find_element(*CartPageLocator.TOTAL_PROD).text.replace('$', '')) and
               shipping_price == float(self.driver.find_element(*CartPageLocator.TOTAL_SHIPPING).text.replace('$', '')) and
               grand_total == float(self.driver.find_element(*CartPageLocator.SUB_TOTAL).text.replace('$', '')) and
               grand_total == float(self.driver.find_element(*CartPageLocator.TOTAL_PRICE).text.replace('$', '')))

    def add_product_item(self):
        '''Adds a product from the first line of the cart. QTY should be 2.
        returns (tuple): (<item qty>, <total item price>)'''
        self.hover(*CartPageLocator.FIRST_ROW_ADD)
        self.click(*CartPageLocator.FIRST_ROW_ADD)
        # Wait a bit for the qty to register.
        time.sleep(1)
        assert(self.visible(*CartPageLocator.FIRST_ROW_QTY))
        assert(self.visible(*CartPageLocator.FIRST_ROW_TOTAL))
        return (int(self.driver.find_element(*CartPageLocator.FIRST_ROW_QTY).get_attribute('value')),
                float(self.driver.find_element(*CartPageLocator.FIRST_ROW_TOTAL).text.replace('$', '')))

    def delete_product_item(self):
        '''Subtracts a product from the first line in the cart. QTY should be 1.
        returns (tuple): (<item qty>, <total item price>)'''
        self.hover(*CartPageLocator.FIRST_ROW_SUBTRACT)
        self.click(*CartPageLocator.FIRST_ROW_SUBTRACT)
        # Wait a bit for the qty to register.
        time.sleep(1)
        assert(self.visible(*CartPageLocator.FIRST_ROW_QTY))
        assert(self.visible(*CartPageLocator.FIRST_ROW_TOTAL))
        return (int(self.driver.find_element(*CartPageLocator.FIRST_ROW_QTY).get_attribute('value')),
                float(self.driver.find_element(*CartPageLocator.FIRST_ROW_TOTAL).text.replace('$', '')))

    def remove_product_item(self):
        '''Removes to the first line product item.'''
        self.hover(*CartPageLocator.FIRST_ROW_SUBTRACT)
        self.click(*CartPageLocator.FIRST_ROW_SUBTRACT)

    def checkout(self):
        '''Click on the checkout button.'''
        self.hover(*CartPageLocator.TO_CHECKOUT)
        self.click(*CartPageLocator.TO_CHECKOUT)

    def is_address_page(self):
        '''Are we in the address page whcih shows authentication worked with cart items.'''
        return self.visible(*CartPageLocator.ADDRESS)
