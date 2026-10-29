import allure
from locators.base_locators import BaseLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

from config import BASE_URL, UI_TIMEOUT


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, UI_TIMEOUT)

    @allure.step("Открыть страницу: {path}")
    def open(self, path="/"):
        self.driver.get(BASE_URL + path)

    def find_visible(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        def try_click(driver):
            overlays = driver.find_elements(
                *BaseLocators.MODAL_OVERLAY
            )
            if any(overlay.is_displayed() for overlay in overlays):
                return False

            element = EC.element_to_be_clickable(locator)(driver)
            if not element:
                return False

            element.click()
            return True

        WebDriverWait(
            self.driver,
            UI_TIMEOUT,
            ignored_exceptions=(
                ElementClickInterceptedException,
                StaleElementReferenceException,
            ),
        ).until(
            try_click,
            message=f"Не удалось кликнуть по элементу: {locator}",
        )

    def fill(self, locator, value):
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(value)

    def get_text(self, locator):
        return self.find_visible(locator).text

    def wait_until_hidden(self, locator):
        return self.wait.until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_for_url(self, url):
        return self.wait.until(EC.url_to_be(url))