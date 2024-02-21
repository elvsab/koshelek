import pytest
from selenium.webdriver.common.by import By


@pytest.fixture()
def shadow_root_wrapper(selenium):
    return selenium.find_element(By.CSS_SELECTOR, 'div.remoteComponent')

@pytest.fixture()
def shadow_root(selenium, shadow_root_wrapper):
    return selenium.execute_script("return arguments[0].shadowRoot", shadow_root_wrapper)