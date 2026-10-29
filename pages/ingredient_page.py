import allure
from selenium.webdriver import ActionChains

from locators.base_locators import BaseLocators
from locators.ingredient_locators import IngredientLocators
from pages.base_page import BasePage


class IngredientPage(BasePage):
    @allure.step("Открыть детали первого ингредиента")
    def open_ingredient_details(self):
        self.click(IngredientLocators.FIRST_CARD)
        self.find_visible(IngredientLocators.OPEN_MODAL)

    @allure.step("Получить заголовок окна ингредиента")
    def get_details_heading(self):
        return self.get_text(IngredientLocators.DETAILS_HEADING)

    @allure.step("Закрыть детали ингредиента крестиком")
    def close_ingredient_details(self):
        button = self.wait.until(
            lambda driver: next(
                (
                    element
                    for element in driver.find_elements(
                        *IngredientLocators.CLOSE_BUTTON
                    )
                    if element.is_displayed() and element.is_enabled()
                ),
                False,
            )
        )
        button.click()
        self.wait_until_hidden(IngredientLocators.OPEN_MODAL)

    def is_details_closed(self):
        return not any(
            element.is_displayed()
            for element in self.driver.find_elements(
                *IngredientLocators.OPEN_MODAL
            )
        )

    @allure.step("Получить счётчик первой булочки")
    def get_bun_counter(self):
        return int(
            self.find_visible(
                IngredientLocators.FIRST_CARD_COUNTER
            ).text
        )

    @allure.step("Перетащить первую булочку в конструктор")
    def add_bun_to_constructor(self):
        def page_is_ready(driver):
            overlays = driver.find_elements(
                *BaseLocators.MODAL_OVERLAY
            )
            return not any(
                overlay.is_displayed() for overlay in overlays
            )

        self.wait.until(page_is_ready)

        source = self.find_visible(IngredientLocators.FIRST_CARD)
        target = self.find_visible(
            IngredientLocators.CONSTRUCTOR_DROP_AREA
        )

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

    @allure.step("Дождаться значения счётчика: {expected}")
    def wait_for_bun_counter(self, expected):
        def counter_matches(driver):
            counters = driver.find_elements(
                *IngredientLocators.FIRST_CARD_COUNTER
            )
            return bool(counters) and counters[0].text == str(expected)

        self.wait.until(
            counter_matches,
            message=f"Счётчик булочки не стал равен {expected}",
        )