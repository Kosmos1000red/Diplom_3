import allure

from locators.order_locators import OrderLocators
from pages.navigation_page import NavigationPage


class FeedPage(NavigationPage):
    @allure.step("Получить количество заказов за всё время")
    def get_total(self):
        return self.wait_for_number(OrderLocators.TOTAL_COUNTER)

    @allure.step("Дождаться увеличения общего счётчика")
    def wait_for_total_increase(self, before):
        self.wait_for_number(
            OrderLocators.TOTAL_COUNTER,
            predicate=lambda value: value > before,
            timeout=60,
            message=f"Общий счётчик не увеличился относительно {before}",
        )

    @allure.step("Получить количество заказов за сегодня")
    def get_today(self):
        return self.wait_for_number(OrderLocators.TODAY_COUNTER)

    @allure.step("Дождаться увеличения счётчика за сегодня")
    def wait_for_today_increase(self, before):
        self.wait_for_number(
            OrderLocators.TODAY_COUNTER,
            predicate=lambda value: value > before,
            timeout=60,
            message=f"Счётчик за сегодня не увеличился относительно {before}",
        )

    @allure.step("Получить номера заказов в работе")
    def get_in_progress_numbers(self):
        return self.get_numbers(OrderLocators.IN_PROGRESS_NUMBERS)

    @allure.step("Дождаться заказа {order_number} в колонке «В работе»")
    def wait_for_order_in_progress(self, order_number):
        self.wait_for_number_in_list(
            OrderLocators.IN_PROGRESS_NUMBERS,
            order_number,
            timeout=20,
        )