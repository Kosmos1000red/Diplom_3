import allure

from pages.navigation_page import NavigationPage


@allure.feature("Основная функциональность")
class TestNavigation:
    @allure.title("Переход в конструктор по клику в шапке")
    def test_go_to_constructor(self, driver):
        page = NavigationPage(driver)
        page.open("/feed")

        page.go_to_constructor()

        assert page.get_constructor_heading() == "Соберите бургер"

    @allure.title("Переход в ленту заказов по клику в шапке")
    def test_go_to_order_feed(self, driver):
        page = NavigationPage(driver)
        page.open("/")

        page.go_to_order_feed()

        assert page.get_order_feed_heading() == "Лента заказов"