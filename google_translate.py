from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.PhantomJS()

'''FIREFOX
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
'''

def translate(text, destination_language, source_language="auto"):
    """
    Translates the given text into the chosen language by scraping Google Translate with Selenium.

    Returns a string with the text translated.\n
    Returns "An error occured while translating: translation not found." if the translation was not found in the webpage. This might come from a mistyped language code.
    """
    try:
        driver.get(f"https://translate.google.com/?hl=en#view=home&op=translate&sl={source_language}&tl={destination_language}&text={text}")
        driver.refresh()
        result = driver.find_element_by_class_name("tlid-translation")
        return result.text
    except NoSuchElementException:
        return "An error occured while translating: translation not found."
    except:
        return "An error occured while translating: unknown error."

def detect_language(text, result_language='en'):
    """
    Returns the language of the given text.
    """
    driver.get(f"https://translate.google.com/?hl={result_language}#view=home&op=translate&sl=auto&tl=en&text={text}")
    driver.refresh()
    raw_result = driver.find_element_by_class_name("jfk-button-checked").get_attribute('innerHTML')
    result = raw_result.split(' - ')[0]
    if result == 'Detect language':
        result = detect_language(text)
    return result
