from selenium.webdriver.common.by import By


class OrderLocators:
    CREATE_ORDER_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Оформить заказ']",
    )
    ORDER_NUMBER = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal_opened'] "
        "h2[class*='Modal_modal__title_shadow']",
    )
    CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal_opened'] "
        "button[class*='Modal_modal__close_modified']",
    )
    TOTAL_COUNTER = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за все время:']"
        "/following-sibling::p",
    )
    TODAY_COUNTER = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за сегодня:']"
        "/following-sibling::p",
    )
    IN_PROGRESS_NUMBERS = (
        By.CSS_SELECTOR,
        "ul[class*='OrderFeed_orderListReady'] li",
    )