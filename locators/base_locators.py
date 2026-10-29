from selenium.webdriver.common.by import By


class BaseLocators:
    MODAL_OVERLAY = (
        By.CSS_SELECTOR,
        "[class*='Modal_modal_overlay']",
    )