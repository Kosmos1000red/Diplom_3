from selenium.webdriver.common.by import By


class LoginLocators:
    EMAIL = (
        By.CSS_SELECTOR,
        "form input[type='text']",
    )
    PASSWORD = (
        By.CSS_SELECTOR,
        "form input[type='password']",
    )
    LOGIN_BUTTON = (
        By.XPATH,
        "//form//button[normalize-space()='Войти']",
    )
    CREATE_ORDER_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Оформить заказ']",
    )