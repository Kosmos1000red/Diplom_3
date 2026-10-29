import os

import allure
import pytest
from selenium import webdriver
from uuid import uuid4

import requests

from config import BASE_URL, REQUEST_TIMEOUT
from pages.login_page import LoginPage


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    os.environ["SE_SKIP_DRIVER_IN_PATH"] = "true"

    if request.param == "chrome":
        browser = webdriver.Chrome()
    else:
        browser = webdriver.Firefox()

    browser.set_window_size(1920, 1080)
    allure.dynamic.parameter("browser", request.param)

    try:
        yield browser
    finally:
        browser.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        if browser is not None:
            allure.attach(
                browser.get_screenshot_as_png(),
                name="Страница в момент падения",
                attachment_type=allure.attachment_type.PNG,
            )

@pytest.fixture
def registered_user():
    unique_id = uuid4().hex
    data = {
        "email": f"ui_{unique_id}@example.com",
        "password": f"Password_{unique_id}",
        "name": "Тестовый пользователь",
    }

    response = requests.post(
        BASE_URL + "/api/auth/register",
        json=data,
        timeout=REQUEST_TIMEOUT,
    )
    assert response.status_code == 200, response.text

    body = response.json()
    token = body["accessToken"]

    try:
        yield data
    finally:
        delete_response = requests.delete(
            BASE_URL + "/api/auth/user",
            headers={"Authorization": token},
            timeout=REQUEST_TIMEOUT,
        )
        assert delete_response.status_code == 202, (
            "Не удалось удалить пользователя: "
            f"{delete_response.status_code}, "
            f"{delete_response.text}"
        )

@pytest.fixture
def authenticated_driver(driver, registered_user):
    page = LoginPage(driver)
    page.login(
        registered_user["email"],
        registered_user["password"],
    )

    return driver