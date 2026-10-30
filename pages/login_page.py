import allure

from config import BASE_URL
from locators.login_locators import LoginLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    @allure.step("Войти под тестовым пользователем")
    def login(self, email, password):
        self.open("/login")
        self.fill(LoginLocators.EMAIL, email)
        self.fill(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.LOGIN_BUTTON)

        self.wait_for_url(BASE_URL + "/")
        self.find_visible(LoginLocators.CREATE_ORDER_BUTTON)