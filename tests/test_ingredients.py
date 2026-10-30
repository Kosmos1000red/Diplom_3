import allure

from pages.ingredient_page import IngredientPage


@allure.feature("Основная функциональность")
class TestIngredients:
    @allure.title("Открытие окна деталей ингредиента")
    def test_open_ingredient_details(self, driver):
        page = IngredientPage(driver)
        page.open("/")

        page.open_ingredient_details()

        assert page.get_details_heading() == "Детали ингредиента"

    @allure.title("Закрытие окна ингредиента крестиком")
    def test_close_ingredient_details(self, driver):
        page = IngredientPage(driver)
        page.open("/")
        page.open_ingredient_details()

        page.close_ingredient_details()

        assert page.is_details_closed()

    @allure.title("Счётчик булочки увеличивается после добавления")
    def test_bun_counter_increases(self, driver):
        page = IngredientPage(driver)
        page.open("/")
        before = page.get_bun_counter()

        page.add_bun_to_constructor()
        page.wait_for_bun_counter(before + 2)

        assert page.get_bun_counter() == before + 2