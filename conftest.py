import os
from uuid import uuid4

import allure
import pytest
import requests
from selenium import webdriver

from config import BASE_URL, REQUEST_TIMEOUT
from pages.login_page import LoginPage


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    os.environ["SE_SKIP_DRIVER_IN_PATH"] = "true"

    if request.param == "chrome":
        browser = webdriver.Chrome()
    else:
        browser = webdriver.Firefox()

    try:
        browser.set_window_size(1920, 1080)
        allure.dynamic.parameter("browser", request.param)
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
    response.raise_for_status()

    body = response.json()
    token = body.get("accessToken")

    if not token:
        raise RuntimeError(
            f"Не получен токен тестового пользователя: {response.text}"
        )

    try:
        yield data
    finally:
        delete_response = requests.delete(
            BASE_URL + "/api/auth/user",
            headers={"Authorization": token},
            timeout=REQUEST_TIMEOUT,
        )
        delete_response.raise_for_status()


@pytest.fixture
def authenticated_driver(driver, registered_user):
    page = LoginPage(driver)
    page.login(
        registered_user["email"],
        registered_user["password"],
    )

    return driver