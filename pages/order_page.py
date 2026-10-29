import allure
from selenium.webdriver.support.ui import WebDriverWait

from locators.ingredient_locators import IngredientLocators
from locators.order_locators import OrderLocators
from pages.ingredient_page import IngredientPage


class OrderPage(IngredientPage):
    @allure.step("Собрать и оформить заказ через интерфейс")
    def create_order(self):
        self.add_bun_to_constructor()
        self.wait_for_bun_counter(2)
        self.click(OrderLocators.CREATE_ORDER_BUTTON)

        def order_number_is_ready(driver):
            elements = driver.find_elements(*OrderLocators.ORDER_NUMBER)
            for element in elements:
                text = element.text.strip()
                if (
                    element.is_displayed()
                    and text.isdigit()
                    and int(text) > 0
                    and text != "9999"
                ):
                    return int(text)
            return False

        return WebDriverWait(self.driver, 60).until(
            order_number_is_ready,
            message="Не появился номер оформленного заказа",
        )

    @allure.step("Закрыть окно оформленного заказа")
    def close_order(self):
        button = self.wait.until(
            lambda driver: next(
                (
                    element
                    for element in driver.find_elements(
                        *OrderLocators.CLOSE_BUTTON
                    )
                    if element.is_displayed() and element.is_enabled()
                ),
                False,
            )
        )
        button.click()
        self.wait_until_hidden(IngredientLocators.OPEN_MODAL)