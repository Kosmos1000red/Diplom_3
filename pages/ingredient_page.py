import allure

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
        self.click(
            IngredientLocators.CLOSE_BUTTON,
            wait_for_overlay=False,
        )
        self.wait_until_hidden(IngredientLocators.OPEN_MODAL)

    def is_details_closed(self):
        return not self.is_any_visible(IngredientLocators.OPEN_MODAL)

    @allure.step("Получить счётчик первой булочки")
    def get_bun_counter(self):
        return self.wait_for_number(
            IngredientLocators.FIRST_CARD_COUNTER
        )

    @allure.step("Перетащить первую булочку в конструктор")
    def add_bun_to_constructor(self):
        self.drag_and_drop(
            IngredientLocators.FIRST_CARD,
            IngredientLocators.CONSTRUCTOR_DROP_AREA,
        )

    @allure.step("Дождаться значения счётчика: {expected}")
    def wait_for_bun_counter(self, expected):
        self.wait_for_number(
            IngredientLocators.FIRST_CARD_COUNTER,
            predicate=lambda value: value == expected,
            message=f"Счётчик булочки не стал равен {expected}",
        )