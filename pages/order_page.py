import allure

from locators.ingredient_locators import IngredientLocators
from locators.order_locators import OrderLocators
from pages.ingredient_page import IngredientPage


class OrderPage(IngredientPage):
    @allure.step("Собрать и оформить заказ через интерфейс")
    def create_order(self):
        self.add_bun_to_constructor()
        self.wait_for_bun_counter(2)
        self.click(OrderLocators.CREATE_ORDER_BUTTON)

        return self.wait_for_number(
            OrderLocators.ORDER_NUMBER,
            predicate=lambda value: value > 0 and value != 9999,
            timeout=60,
            message="Не появился номер оформленного заказа",
        )

    @allure.step("Закрыть окно оформленного заказа")
    def close_order(self):
        self.click(
            OrderLocators.CLOSE_BUTTON,
            wait_for_overlay=False,
        )
        self.wait_until_hidden(IngredientLocators.OPEN_MODAL)