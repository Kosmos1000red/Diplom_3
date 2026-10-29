import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait

from locators.order_locators import OrderLocators
from pages.navigation_page import NavigationPage


class FeedPage(NavigationPage):
    def _read_counter(self, locator):
        def read(driver):
            elements = driver.find_elements(*locator)
            if not elements:
                return False

            text = "".join(elements[0].text.split())
            if not text.isdigit():
                return False

            return (int(text),)

        return self.wait.until(read)[0]

    def _wait_for_counter_increase(self, locator, before):
        def increased(driver):
            elements = driver.find_elements(*locator)
            if not elements:
                return False

            text = "".join(elements[0].text.split())
            return text.isdigit() and int(text) > before

        WebDriverWait(
            self.driver,
            60,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(
            increased,
            message=f"Счётчик не увеличился относительно {before}",
        )

    @allure.step("Получить количество заказов за всё время")
    def get_total(self):
        return self._read_counter(OrderLocators.TOTAL_COUNTER)

    @allure.step("Дождаться увеличения общего счётчика")
    def wait_for_total_increase(self, before):
        self._wait_for_counter_increase(
            OrderLocators.TOTAL_COUNTER, before
        )

    @allure.step("Получить количество заказов за сегодня")
    def get_today(self):
        return self._read_counter(OrderLocators.TODAY_COUNTER)

    @allure.step("Дождаться увеличения счётчика за сегодня")
    def wait_for_today_increase(self, before):
        self._wait_for_counter_increase(
            OrderLocators.TODAY_COUNTER, before
        )

    @allure.step("Получить номера заказов в работе")
    def get_in_progress_numbers(self):
        numbers = []

        for element in self.driver.find_elements(
            *OrderLocators.IN_PROGRESS_NUMBERS
        ):
            text = element.text.strip()
            if text.isdigit():
                numbers.append(int(text))

        return numbers

    @allure.step("Дождаться заказа {order_number} в колонке «В работе»")
    def wait_for_order_in_progress(self, order_number):
        WebDriverWait(
            self.driver,
            20,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(
            lambda driver: (
                order_number in self.get_in_progress_numbers()
            ),
            message=(
                f"Заказ {order_number} не появился "
                "в колонке «В работе»"
            ),
        )