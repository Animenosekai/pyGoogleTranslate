"""
pyGoogleTranslate

--> A Google Translate webpage parser for Python 3

⚠️ Do not forget to set the used browser with browser()\n
⚠️ Do not forget to call browser_kill() after using pyGoogleTranslate (at the end of your script/when you stop your script)\n
Without browser_kill(), your browser will stay opened until you close it in your activity monitor (unless it is phantomjs). 

© Anime no Sekai - 2020
"""

import warnings
import psutil
from lifeeasy import write_file, today, current_time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from internal.caching import search_translation_cache, add_translation_cache
from internal.language_code import verify_language_code
from internal import google_translate_data


class BrowserError(Exception):
    """
    When the browser isn't available.
    """
    def __init__(self, msg=None):
        self.msg = msg 
    def __str__(self):
        exception_msg = f"\n\n⚠️ ⚠️ ⚠️\n{self.msg}\n"
        return exception_msg


warnings.filterwarnings('ignore')

driver_name = ''
driver = None
connected = False
last_translation = ''

def browser(browser_name, executable_path="PATH"):
    """
    To choose the headless browser used by pyGoogleTranslate.\n
    <executable_path> sets the executable path for your browser.\n
    If <executable_path> is empty, pyGoogleTranslate will consider that the browser driver/executable is in your PATH (for example if you downloaded the driver with Homebrew).\n
    Browser options:
        Firefox
        Chrome
        PhantomJS
    ⚠️ Do not forget to call browser_kill() after using pyGoogleTranslate (at the end of your script/when you stop your script)\n
    Without browser_kill(), your browser will stay opened until you close it in your activity monitor (unless it is phantomjs). 
    """
    global driver
    global driver_name
    global connected
    if connected:
        browser_kill()
    if browser_name.lower() == 'firefox':
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.headless = True
        if executable_path == 'PATH':
            driver = webdriver.Firefox(options=options)
            connected = True
        else:
            driver = webdriver.Firefox(options=options, executable_path=executable_path)
            connected = True
        driver_name = 'Firefox'
    elif browser_name.lower() == 'chrome':
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        #chrome_options.add_argument("--no-sandbox")
        if executable_path == 'PATH':
            driver = webdriver.Chrome(options=chrome_options)
            connected = True
        else:
            driver = webdriver.Chrome(options=chrome_options, executable_path=executable_path)
            connected = True
        driver_name = 'Chrome'
    elif browser_name.lower() == 'phantom':
        if executable_path == 'PATH':
            driver = webdriver.PhantomJS()
            connected = True
        else:
            driver = webdriver.PhantomJS(executable_path=executable_path)
            connected = True
        driver_name = 'PhantomJS'
    elif browser_name.lower() == 'phantomjs':
        if executable_path == 'PATH':
            driver = webdriver.PhantomJS()
            connected = True
        else:
            driver = webdriver.PhantomJS(executable_path=executable_path)
            connected = True
        driver_name = 'PhantomJS'
    else:
        raise BrowserError(f'{browser_name} is not supported yet.')

def browser_kill():
    """
    Kills the browser process in use.
    """
    global connected
    if driver_name == 'Chrome' or driver_name == 'Firefox':
        driver_process = psutil.Process(driver.service.process.pid)
        if driver_process.is_running():
            process = driver_process.children()
            if process:
                process = process[0]
                if process.is_running():
                    driver.quit()
                else:
                    process.kill()
            connected = False

def translate(text, destination_language, source_language="auto", cache=False, debug=False):
    """
    Translates the given text into the chosen language by scraping Google Translate with Selenium.

    Returns a string with the text translated.\n
    Returns "An error occured while translating: translation not found." if the translation was not found in the webpage. This might come from a mistyped language code.
    """
    from internal.domain import gt_domain
    global last_translation
    if debug:
        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Starting Translation...\n', append=True)
    if debug:
        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Searching Caches...\n', append=True)
    cache_result = search_translation_cache(source_language=source_language, destination_language=destination_language, source=text)
    if not cache_result is None:
        if debug:
            line_number = cache_result['line_number']
            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Translation found in Caches (line {line_number})\n', append=True)
        return cache_result['result']
    else:
        if driver is None:
            if debug:
                write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - No driver selected\n', append=True)
            raise BrowserError("Browser is not set yet.\n Please set it with browser()")
        if not connected:
            if debug:
                write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Driver disconnected, last driver: {driver_name}\n', append=True)
            raise BrowserError(f'You disconnected the last browser in use ({driver_name}).\n Please reconnect one with browser()')
        else:
            if debug:
                write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - First attempt url is: https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}\n', append=True)
            driver.get(f"https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}")
            try:
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                result = driver.find_element_by_class_name("tlid-translation")
                if result.text == last_translation or result.text == str(last_translation + '...'):
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Translation not finished detected... Refreshing page before new attempt...\n', append=True)
                    driver.refresh()
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                    result = driver.find_element_by_class_name("tlid-translation")
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Setting last_translation global variable to new translation...\n', append=True)
                last_translation = str(result.text)
                if cache:
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Adding result to cache...\n', append=True)
                    add_translation_cache(source_language=source_language, destination_language=destination_language, source=text, result=str(result.text))
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Returning value... {result.text}\n', append=True)
                return str(result.text)
            except NoSuchElementException:
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Element not found on page...\n', append=True)
                try:
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] New attempt...\n', append=True)
                    driver.get(f"https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}")
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                    result = driver.find_element_by_class_name("tlid-translation")
                    if result.text == last_translation or result.text == str(last_translation + '...'):
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Translation not finished detected... Refreshing page before new attempt...\n', append=True)
                        driver.refresh()
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                        result = driver.find_element_by_class_name("tlid-translation")
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Setting last_translation global variable to new translation...\n', append=True)
                    last_translation = str(result.text)
                    if cache:
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Adding result to cache...\n', append=True)
                        add_translation_cache(source_language=source_language, destination_language=destination_language, source=text, result=str(result.text))
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Returning value... {result.text}\n', append=True)
                    return str(result.text)
                except NoSuchElementException:
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Element not found on page...\n', append=True)
                    try:
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] New attempt...\n', append=True)
                        driver.get(f"https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}")
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Translation not finished detected... Refreshing page before new attempt...\n', append=True)
                        driver.refresh()
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                        result = driver.find_element_by_class_name("tlid-translation")
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Setting last_translation global variable to new translation...\n', append=True)
                        last_translation = str(result.text)
                        if cache:
                            if debug:
                                write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Adding result to cache...\n', append=True)
                            add_translation_cache(source_language=source_language, destination_language=destination_language, source=text, result=str(result.text))
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Returning value... {result.text}\n', append=True)
                        return str(result.text)
                    except NoSuchElementException:
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Element not found, aborting...\n', append=True)
                        return "An error occured while translating: translation not found."
                    except Exception as e:
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Unknown error\n', append=True)
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Error details: {str(e)}\n', append=True)
                        return "An error occured while translating: unknown error."
                except Exception as e:
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Unknown error\n', append=True)
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Error details: {str(e)}\n', append=True)
                    return "An error occured while translating: unknown error."
            except Exception as e:
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Unknown error\n', append=True)
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Error details: {str(e)}\n', append=True)
                try:
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] New attempt...\n', append=True)
                    driver.get(f"https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}")
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                    result = driver.find_element_by_class_name("tlid-translation")
                    if result.text == last_translation or result.text == str(last_translation + '...'):
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Translation not finished detected... Refreshing page before new attempt...\n', append=True)
                        driver.refresh()
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                        result = driver.find_element_by_class_name("tlid-translation")
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Setting last_translation global variable to new translation...\n', append=True)
                    last_translation = str(result.text)
                    if cache:
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Adding result to cache...\n', append=True)
                        add_translation_cache(source_language=source_language, destination_language=destination_language, source=text, result=str(result.text))
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Returning value... {result.text}\n', append=True)
                    return str(result.text)
                except Exception as e:
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Unknown error\n', append=True)
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Error details: {str(e)}\n', append=True)
                    return "An error occured while translating: unknown error."

def detect_language(text, result_language='en'):
    """
    Returns the language of the given text.
    """
    from internal.domain import gt_domain
    if driver is None:
        raise BrowserError("Browser is not set yet.\n Please set it with browser()")
    if not connected:
        raise BrowserError(f'You disconnected the last browser in use ({driver_name}).\n Please reconnect one with browser()')
    else:
        try:
            driver.get(f"https://{gt_domain}/?hl={verify_language_code(result_language)}#view=home&op=translate&sl=auto&tl=en&text={str(text)}")
            driver.refresh()
            raw_result = driver.find_element_by_class_name("jfk-button-checked").get_attribute('innerHTML')
            result = raw_result.split(' - ')[0]
            if result == 'Detect language':
                result = detect_language(text, result_language=result_language)
            return str(result)
        except:
            return "An error occured while detecting the language.\nPlease try again."
            
def transliterate(text, source_language="auto"):
    """
    Returns the transliteration provided by Google Translate (if available)\n
    i.e Ohayou --> おはよう / おはよう --> Ohayou
    """
    from internal.domain import gt_domain
    if driver is None:
        raise BrowserError("Browser is not set yet.\n Please set it with browser()")
    if not connected:
        raise BrowserError(f'You disconnected the last browser in use ({driver_name}).\n Please reconnect one with browser()')
    else:
        try:
            driver.get(f'https://{gt_domain}/#view=home&op=translate&sl={verify_language_code(source_language)}&tl=en&text={str(text)}')
            driver.refresh()
            result = driver.find_element_by_class_name('tlid-transliteration-content')
            return str(result.text)
        except:
            return 'not available'

def definition(text, source_language="auto"):
    """
    Returns the word type (i.e Interjection, Noun), defintion (if available) and sentence example where the word could be used (if available)
    """
    from internal.domain import gt_domain
    if driver is None:
        raise BrowserError("Browser is not set yet.\n Please set it with browser()")
    if not connected:
        raise BrowserError(f'You disconnected the last browser in use ({driver_name}).\n Please reconnect one with browser()')
    else:
        driver.get(f'https://{gt_domain}/#view=home&op=translate&sl={verify_language_code(source_language)}&tl=en&text={str(text)}')
        driver.refresh()
        final_dict = {}
        try:
            word_type = driver.find_element_by_class_name('gt-cd-pos').text
        except:
            word_type = 'not available.'
        try:
            word_definition = driver.find_element_by_class_name('gt-def-row').text
        except:
            word_definition = 'not available.'
        try:
            example = driver.find_element_by_class_name('gt-def-example').text
        except:
            example = 'not available.'
        final_dict['word_type'] = str(word_type)
        final_dict['definition'] = str(word_definition)
        final_dict['example'] = str(example)
        return final_dict