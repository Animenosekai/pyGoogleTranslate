"""
pyGoogleTranslate

--> A Google Translate webpage parser for Python 3

⚠️ Do not forget to set the used browser with browser()

© Anime no Sekai - 2020
"""

import warnings

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class BrowserError(Exception):
    """
    When the browser isn't available.
    """
    def __init__(self, msg=None):
        self.msg = msg 
    def __str__(self):
        exception_msg = f"\n\n⚠️⚠️⚠️\n{self.msg}\n"
        return exception_msg

warnings.filterwarnings('ignore')

driver = None

def browser(browser_name, executable_path="PATH"):
    """
    To choose the headless browser used by pyGoogleTranslate.\n
    <executable_path> sets the executable path for your browser.\n
    If <executable_path> is not empty, pyGoogleTranslate will consider that the browser driver/executable is in your PATH (for example if you downloaded the driver with Homebrew).
    Browser options:
        Firefox
        Chrome
        PhantomJS
    """
    global driver
    if browser_name.lower() == 'firefox':
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.headless = True
        if executable_path == 'PATH':
            driver = webdriver.Firefox(options=options)
        else:
            driver = webdriver.Firefox(options=options, executable_path=executable_path)
    elif browser_name.lower() == 'chrome':
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        #chrome_options.add_argument("--no-sandbox")
        if executable_path == 'PATH':
            driver = webdriver.Chrome(options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options, executable_path=executable_path)
    elif browser_name.lower() == 'phantom':
        if executable_path == 'PATH':
            driver = webdriver.PhantomJS()
        else:
            driver = webdriver.PhantomJS(executable_path=executable_path)
    elif browser_name.lower() == 'phantomjs':
        if executable_path == 'PATH':
            driver = webdriver.PhantomJS()
        else:
            driver = webdriver.PhantomJS(executable_path=executable_path)
    else:
        raise BrowserError(f'{browser_name} is not supported yet.')

def translate(text, destination_language, source_language="auto"):
    """
    Translates the given text into the chosen language by scraping Google Translate with Selenium.

    Returns a string with the text translated.\n
    Returns "An error occured while translating: translation not found." if the translation was not found in the webpage. This might come from a mistyped language code.
    """
    if driver is None:
        raise BrowserError("Browser is not set yet.\n Please set it with browser()")
    else:
        try:
            driver.get(f"https://translate.google.com/?hl=en#view=home&op=translate&sl={source_language}&tl={destination_language}&text={str(text)}")
            driver.refresh()
            result = driver.find_element_by_class_name("tlid-translation")
            return str(result.text)
        except NoSuchElementException:
            return "An error occured while translating: translation not found."
        except:
            return "An error occured while translating: unknown error."

def detect_language(text, result_language='en'):
    """
    Returns the language of the given text.
    """
    if driver is None:
        raise BrowserError("Browser is not set yet.\n Please set it with browser()")
    else:
        driver.get(f"https://translate.google.com/?hl={result_language}#view=home&op=translate&sl=auto&tl=en&text={str(text)}")
        driver.refresh()
        raw_result = driver.find_element_by_class_name("jfk-button-checked").get_attribute('innerHTML')
        result = raw_result.split(' - ')[0]
        if result == 'Detect language':
            result = detect_language(text, result_language=result_language)
        return str(result)
