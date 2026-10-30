import allure

from pages.feed_page import FeedPage
from pages.order_page import OrderPage


@allure.feature("Лента заказов")
class TestFeed:
    @allure.title("Общий счётчик увеличивается после создания заказа")
    def test_total_counter_increases(self, authenticated_driver):
        feed = FeedPage(authenticated_driver)
        feed.go_to_order_feed()
        before = feed.get_total()

        feed.go_to_constructor()
        order = OrderPage(authenticated_driver)
        order.create_order()
        order.close_order()

        feed.go_to_order_feed()
        feed.wait_for_total_increase(before)

        assert feed.get_total() > before

    @allure.title("Счётчик за сегодня увеличивается после создания заказа")
    def test_today_counter_increases(self, authenticated_driver):
        feed = FeedPage(authenticated_driver)
        feed.go_to_order_feed()
        before = feed.get_today()

        feed.go_to_constructor()
        order = OrderPage(authenticated_driver)
        order.create_order()
        order.close_order()

        feed.go_to_order_feed()
        feed.wait_for_today_increase(before)

        assert feed.get_today() > before

    @allure.title("Номер нового заказа появляется в колонке «В работе»")
    def test_order_appears_in_progress(self, authenticated_driver):
        order = OrderPage(authenticated_driver)

        order_number = order.create_order()
        order.close_order()

        feed = FeedPage(authenticated_driver)
        feed.go_to_order_feed()
        feed.wait_for_order_in_progress(order_number)

        assert order_number in feed.get_in_progress_numbers()