import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from constants import shadow_root, shadow_root_wrapper

def test_invalid_login(selenium, shadow_root):
    login_input = shadow_root.find_element(By.CSS_SELECTOR,
                                           'div[data-wi="user-name"][data-pw="auth-widget-signup-form"]')

    # Негативные сценарии
    scenarios = [
        ('12345', 'Short login'),
        ('username123456789012345678901234567890123456', 'Long login'),
        ('username!@#$', 'Invalid characters'),
        ('1username', 'Starts with number'),
        ('юзернейм', 'Non-Latin characters'),
        ('existing_username', 'Username already taken')
    ]

    for value, scenario_name in scenarios:
        selenium.execute_script("arguments[0].value = '';", login_input)
        selenium.execute_script("arguments[0].value = '{}';".format(value), login_input)
        error_message = shadow_root.find_element(By.CSS_SELECTOR,
                                                 'div[data-wi="message"][data-pw="authorization-base-input-message"]')
        assert error_message.is_displayed(), f"Scenario failed: {scenario_name}"

def test_invalid_email(selenium, shadow_root):
    email_input = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="email"][name="username"]')
    selenium.execute_script("arguments[0].value = 'invalid_email'", email_input)
    error_message = shadow_root.find_element(By.CSS_SELECTOR,
                                             'div[data-wi="message"][data-pw="authorization-base-input-message"]')
    assert error_message.is_displayed() 

def test_email_is_null(selenium, shadow_root):
    email_input = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="email"][name="username"]')
    email_input.send_keys(Keys.RETURN)  # Отправляем пустое значение
    error_message = shadow_root.find_element(By.CSS_SELECTOR, 'div[data-w="authorization-base-input-message"] span.k-text')
    assert "Поле не заполнено" in error_message.text, "Текст ошибки 'Поле не заполнено' не найден"

def test_long_email(selenium, shadow_root):
    email_input = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="email"][name="username"]')
    long_email = "a" * 255 + "@example.com"  # Создаем слишком длинный e-mail
    email_input.clear()
    email_input.send_keys(long_email)
    time.sleep(1)
    other_field = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    other_field.click()
    time.sleep(1)
    try:
        error_message = shadow_root.find_element(By.CSS_SELECTOR,
                                                 'div.v-text-field__details > div.v-messages.theme--light.error--text > div.v-messages__wrapper > div.v-messages__message > div[data-w="authorization-base-input-message"] > div.k-text-k-typography-body-2-regular > span.k-text')
        assert False, "Сообщение об ошибке найдено, хотя не должно быть"
    except NoSuchElementException:
        pass

def test_password_length(selenium, shadow_root):
    for password in ["1234567", "a" * 65]:
        password_input = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="password"][name="new-password"]')
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(1)
        other_field = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="text"]')
        other_field.click()
        time.sleep(1)
        try:
            error_message = shadow_root.find_element(By.CSS_SELECTOR,
                                                     'div.v-text-field__details > div.v-messages.theme--light.error--text > div.v-messages__wrapper > div.v-messages__message > div[data-w="auth-widget-password-input-message"] > div.k-text-kypography-body-2-regular > span.k-text')
            assert False, f"Ошибка не возникла для пароля: {password}"
        except NoSuchElementException:
            pass

def test_password_upper_and_lower(selenium, shadow_root):
    for password in ["onlylowercase", "ONLYUPPERCASE"]:
        password_input = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="password"][name="new-password"]')
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(1)
        other_field = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="text"]')
        other_field.click()
        time.sleep(1)
        try:
            error_message = shadow_root.find_element(By.CSS_SELECTOR,
                                                     'div.v-text-field__details > div.v-messages.theme--light.error--text > div.v-messages__wrapper > div.v-messages__message > div[data-w="auth-widget-password-input-message"] > div.k-text-kypography-body-2-regular > span.k-text')
            assert False, f"Ошибка не возникла для пароля: {password}"
        except NoSuchElementException:
            pass

def test_password_only_digits(selenium, shadow_root):
    password_input = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="password"][name="new-password"]')
    password_input.clear()
    password = "1234567890"
    password_input.send_keys(password)
    time.sleep(1)
    other_field = shadow_root.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    other_field.click()
    time.sleep(1)
    try:
        error_message = shadow_root.find_element(By.CSS_SELECTOR,
                                                 'div.v-messages.theme--light.error--text > div.v-messages__wrapper > div.v-messages__message > div[data-w="auth-widget-password-input-message"] > div.k-text-k-typography-body-2-regular > span.k-text')

        assert "Пароль должен содержать от 8 до 64 символов, включая заглавные буквы и цифры" in error_message.text, "Ошибка не возникла для пароля: {}".format(
            password)
    except NoSuchElementException:
        pass