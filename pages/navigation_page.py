import allure

from config import BASE_URL
from locators.navigation_locators import NavigationLocators
from pages.base_page import BasePage


class NavigationPage(BasePage):
    @allure.step("Перейти в конструктор через шапку")
    def go_to_constructor(self):
        self.click(NavigationLocators.CONSTRUCTOR)
        self.wait_for_url(BASE_URL + "/")

    @allure.step("Перейти в ленту заказов через шапку")
    def go_to_order_feed(self):
        self.click(NavigationLocators.ORDER_FEED)
        self.wait_for_url(BASE_URL + "/feed")

    @allure.step("Получить заголовок конструктора")
    def get_constructor_heading(self):
        return self.get_text(
            NavigationLocators.CONSTRUCTOR_HEADING
        )

    @allure.step("Получить заголовок ленты заказов")
    def get_order_feed_heading(self):
        return self.get_text(
            NavigationLocators.ORDER_FEED_HEADING
        )