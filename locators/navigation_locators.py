from selenium.webdriver.common.by import By


class NavigationLocators:
    CONSTRUCTOR = (
        By.CSS_SELECTOR,
        "header a[href='/']",
    )
    ORDER_FEED = (
        By.CSS_SELECTOR,
        "header a[href='/feed']",
    )
    CONSTRUCTOR_HEADING = (
        By.XPATH,
        "//h1[normalize-space()='Соберите бургер']",
    )
    ORDER_FEED_HEADING = (
        By.XPATH,
        "//h1[normalize-space()='Лента заказов']",
    )