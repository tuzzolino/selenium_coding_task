from selenium.webdriver.common.by import By


class MainPageLocators(object):
    '''A class for main page locators.'''
    # Home page title.
    TITLE = (By.XPATH, '/html/head/title')

    # Home page cart items
    CART_ITEMS = (By.ID, 'homefeatured')
    CART_QUANTITY = (By.XPATH, '//*[@id="header"]/div[3]/div/div/div[3]/div/a/span[1]')
    CART_NO_QUANTITY = (By.XPATH, '//*[@id="header"]/div[3]/div/div/div[3]/div/a/span[5]')

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

    # Sign in.
    SIGN_IN = (By.XPATH, '//*[@id="header"]/div[2]/div/div/nav/div[1]')

    # To Cart Page.
    CART_PAGE = (By.XPATH, '//*[@id="header"]/div[3]/div/div/div[3]/div/a')

class CartPageLocator(object):
    '''A class for the cart page locators'''
    # Change locators
    CART_TABLE = (By.XPATH, '//*[@id="cart_summary"]')
    FIRST_ROW_ADD = (By.XPATH, '//*[@id="cart_quantity_up_1_1_0_0"]')
    FIRST_ROW_SUBTRACT = (By.XPATH, '//*[@id="cart_quantity_down_1_1_0_0"]')
    FIRST_ROW_REMOVE = (By.XPATH, '//*[@id="1_1_0_0"]')
    FIRST_ROW_TOTAL = (By.XPATH, '//*[@id="product_1_1_0_0"]/td[6]')
    FIRST_ROW_QTY = (By.XPATH, '//*[@id="product_1_1_0_0"]/td[5]/input[2]')
    TO_CHECKOUT = (By.XPATH, '//*[@id="center_column"]/p[2]/a[1]')

    TOTAL_PROD = (By.ID, 'total_product')
    TOTAL_SHIPPING = (By.ID, 'total_shipping')
    SUB_TOTAL = (By.ID, 'total_price_without_tax')
    TOTAL_PRICE = (By.ID, 'total_price')

    # Checkout confirmation:
    ADDRESS = (By.XPATH, '//*[@id="center_column"]/h1')

class SearchResultsPageLocators(object):
    '''A class for search results locators.'''

    # View box locators.
    GRID_VIEW = (By.XPATH, '//*[@id="grid"]/a/i')
    LIST_VIEW = (By.XPATH, '//*[@id="list"]/a/i')
    CENTER_COLUMN = (By.XPATH, '//*[@id="center_column"]/ul')
    LIST_OF_SEARCH_ITEMS = (By.XPATH, '//*[@id="center_column"]/ul/li')
    SEARCH_ALERT = (By.XPATH, '//*[@id="center_column"]/p')
    ROW_VIEW = (By.CLASS_NAME, 'row')

class SignInOutLocator(object):
    '''A class for sign in/out locators.'''

    # Interaction locators
    EMAIL_INPUT = (By.XPATH, '//*[@id="email"]')
    PASSWORD_INPUT = (By.XPATH, '//*[@id="passwd"]')
    SUBMIT_BTN = (By.XPATH, '//*[@id="SubmitLogin"]')
    LOGOUT_BTN = (By.XPATH, '//*[@id="header"]/div[2]/div/div/nav/div[2]/a')
    SIGN_IN_BOX = (By.XPATH, '//*[@id="header"]/div[2]/div/div/nav/div[1]/a/span')
    SIGN_IN_BOX_CLICK = (By.XPATH, '//*[@id="header"]/div[2]/div/div/nav/div[1]/a')

    # Confirmation locators.
    # Text to read: 'AUTHENTICATION'
    AUTHENTICATION = (By.XPATH, '//*[@id="center_column"]/h1')

    # Text to read: 'An email address required.' 'Password is required.' 'Invalid email address.' 'Authentication failed.'
    ALERT_TEXT = (By.XPATH, '//*[@id="center_column"]/div[1]/ol/li')

    # Login successful.
    # Text to read: Welcome to your account. Here you can manage all of your personal information and orders.
    LOGGED_IN_TEXT = (By.XPATH, '//*[@id="columns"]/div[1]/span[2]')
