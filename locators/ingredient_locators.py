from selenium.webdriver.common.by import By


class IngredientLocators:
    FIRST_CARD = (
        By.CSS_SELECTOR,
        "a[class*='BurgerIngredient_ingredient__']",
    )
    OPEN_MODAL = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal_opened']",
    )
    DETAILS_HEADING = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]"
        "//h2[normalize-space()='Детали ингредиента']",
    )
    CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal_opened'] "
        "button[class*='Modal_modal__close_modified']",
    )

    FIRST_CARD_COUNTER = (
        By.CSS_SELECTOR,
        "a[class*='BurgerIngredient_ingredient__'] "
        "[class*='counter_counter__num']",
    )
    CONSTRUCTOR_DROP_AREA = (
        By.CSS_SELECTOR,
        "section[class*='BurgerConstructor_basket__']",
    )