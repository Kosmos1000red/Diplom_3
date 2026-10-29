import os

import allure
import pytest
from selenium import webdriver


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