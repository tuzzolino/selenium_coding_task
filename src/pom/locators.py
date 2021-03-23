from selenium.webdriver.common.by import By


class MainPageLocators(object):
    """A class for main page locators."""
    # Home page title.
    TITLE = (By.XPATH, '/html/head/title')

    # Home page cart items
    CART_ITEMS = (By.ID, 'homefeatured')
    CART_QUANTITY = (By.CLASS_NAME, 'ajax_cart_quantity')
    CART_NO_QUANITY = (By.CLASS_NAME, 'ajax_cart_no_product')

    # Hover Items to add to cart.
    BLOCK_PRODUCT = (By.CLASS_NAME, 'ajax_block_product')
    ADD_ITEM_BTN = (By.CLASS_NAME, 'ajax_add_to_cart_button')
    ITEM_PRICE = (By.CLASS_NAME, 'price')
    ITEM_NAME = (By.CLASS_NAME, 'replace-2x')

    # Confirmation Add Modal.
    MODAL_CONFIRM = (By.ID, 'layer_cart')
    CART_PROD_NAME = (By.ID, 'layer_cart_product_title')
    CART_PROD_PRICE = (By.ID, 'layer_cart_product_price')
    CART_PROD_QTY = (By.ID, 'layer_cart_product_quantity')
    TOTAL_QTY = (By.ID, 'layer_cart_product_quantity')
    BLOCK_PROD_TOTAL = (By.CLASS_NAME, 'ajax_block_products_total') 
    SHIPPING_COST = (By.CLASS_NAME, 'ajax_cart_shipping_cost')
    CART_TOTAL = (By.CLASS_NAME, 'ajax_block_cart_total')
    CONT_SHOPPING = (By.CLASS_NAME, 'continue')
    CLOSE_MODAL = (By.CLASS_NAME, 'cross')

    # Search box locators.
    SEARCH_TEXTBOX = (By.XPATH, '//*[@id="search_query_top"]')
    SEARCH_SUBMIT = (By.XPATH, '//*[@id="searchbox"]/button')

class CartPageLocator(object):
    """A class for the cart page locators."""
    CART_TABLE = (By.XPATH, '//*[@id="cart_summary"]')

class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should come here"""

    # View box locators.
    GRID_VIEW = (By.XPATH, '//*[@id="grid"]/a/i')
    LIST_VIEW = (By.XPATH, '//*[@id="list"]/a/i')
    CENTER_COLUMN = (By.XPATH, '//*[@id="center_column"]/ul')
    LIST_OF_SEARCH_ITEMS = (By.XPATH, '//*[@id="center_column"]/ul/li')
    SEARCH_ALERT = (By.XPATH, '//*[@id="center_column"]/p')
    ROW_VIEW = (By.CLASS_NAME, 'row')
