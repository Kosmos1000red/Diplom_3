import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, UI_TIMEOUT
from locators.base_locators import BaseLocators


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, UI_TIMEOUT)

    def wait_until(self, condition, timeout=None, message=""):
        return WebDriverWait(
            self.driver,
            UI_TIMEOUT if timeout is None else timeout,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(
            lambda driver: condition(),
            message=message,
        )

    @allure.step("Открыть страницу: {path}")
    def open(self, path="/"):
        self.driver.get(BASE_URL + path)

    def find_visible(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def is_any_visible(self, locator):
        return any(
            element.is_displayed()
            for element in self.driver.find_elements(*locator)
        )

    def wait_until_hidden(self, locator):
        return self.wait_until(
            lambda: not self.is_any_visible(locator),
            message=f"Элемент не исчез: {locator}",
        )

    def click(self, locator, wait_for_overlay=True):
        def try_click(driver):
            if (
                wait_for_overlay
                and self.is_any_visible(BaseLocators.MODAL_OVERLAY)
            ):
                return False

            elements = driver.find_elements(*locator)
            element = next(
                (
                    item for item in elements
                    if item.is_displayed() and item.is_enabled()
                ),
                None,
            )

            if element is None:
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

    def wait_for_url(self, url):
        return self.wait.until(EC.url_to_be(url))

    def get_numbers(self, locator):
        numbers = []

        for element in self.driver.find_elements(*locator):
            if element.is_displayed():
                text = "".join(element.text.split())
                if text.isdigit():
                    numbers.append(int(text))

        return numbers

    def wait_for_number(
        self,
        locator,
        predicate=None,
        timeout=None,
        message="Не появилось ожидаемое числовое значение",
    ):
        def number_matches():
            numbers = self.get_numbers(locator)
            if not numbers:
                return False

            value = numbers[0]
            if predicate is not None and not predicate(value):
                return False

            return (value,)

        return self.wait_until(
            number_matches,
            timeout=timeout,
            message=message,
        )[0]

    def wait_for_number_in_list(self, locator, number, timeout=None):
        self.wait_until(
            lambda: number in self.get_numbers(locator),
            timeout=timeout,
            message=f"Номер {number} не появился в списке",
        )

    def drag_and_drop(self, source_locator, target_locator):
        self.wait_until_hidden(BaseLocators.MODAL_OVERLAY)

        source = self.find_visible(source_locator)
        target = self.find_visible(target_locator)

        if self.driver.capabilities["browserName"] == "firefox":
            self.driver.execute_script(
                """
                const source = arguments[0];
                const target = arguments[1];
                const transfer = new DataTransfer();

                function dispatch(element, type) {
                    const rect = element.getBoundingClientRect();
                    element.dispatchEvent(new DragEvent(type, {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: transfer,
                        clientX: rect.left + rect.width / 2,
                        clientY: rect.top + rect.height / 2
                    }));
                }

                dispatch(source, "dragstart");
                dispatch(target, "dragenter");
                dispatch(target, "dragover");
                dispatch(target, "drop");
                dispatch(source, "dragend");
                """,
                source,
                target,
            )
        else:
            ActionChains(self.driver).drag_and_drop(
                source, target
            ).perform()