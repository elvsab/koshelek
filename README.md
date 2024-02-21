# koshelek
negative tests for authorization fields. There are 3 .py files : tests, conftest (with fixture for opening main page) and constants (repeating variables for each test) and 1 chromedriver.exe
These tests can be enabled with installed packages :pytest 8.0.1 , pytest-selenium 4.1.0 , requests 2.31.0 , selenium 4.17.2 , webdriver-manager 4.0.1.
To launch these files chromedriver is needed (you can download it from official website https://chromedriver.chromium.org/downloads/version-selection).Using chromedriver for Windows 64 (version dated 24 Feb 2024), browser Google Chrome 121.0.6167.185
To start tests you need to use code - "python -m pytest -v --driver Chrome --driver-path 'your_path_to_chromedriver tests.py'" in Terminal of PyCharm
