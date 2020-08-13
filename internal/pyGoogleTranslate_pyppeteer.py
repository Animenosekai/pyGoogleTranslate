import asyncio
import threading
from pyppeteer import launch
from pyppeteer.errors import ElementHandleError

from lifeeasy import write_file, today, current_time

from .caching import search_translation_cache, add_translation_cache
from .language_code import verify_language_code

last_translation = ''
browser = None
page = None

async def _launch():
    """
    Internal Function to launch pypeteer
    """
    global browser
    global page
    browser = await launch(
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        headless=True,
        args=['--no-sandbox']
    )
    page = await browser.newPage()
    page.setDefaultNavigationTimeout(timeout=0)

if isinstance(threading.current_thread(), threading._MainThread):
    print('Main Thread')
    asyncio.get_event_loop().run_until_complete(_launch())
else:
    print('Not Main Thread')
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.get_event_loop().run_until_complete(_launch())

async def _translate(text, destination_language, source_language="auto", cache=False, debug=False):
    """
    Internal Function to translate
    """
    from .domain import gt_domain
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
        if debug:
            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - First attempt url is: https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}\n', append=True)
        await page.goto(f"https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}")
        try:
            if debug:
                write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Getting DOM Element by Class Name (tlid-translation)\n', append=True)
            result = await page.evaluate("document.getElementsByClassName(\"tlid-translation\")[0].innerText")
            if result == last_translation or result == str(last_translation + '...'):
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Translation not finished detected... Refreshing page before new attempt...\n', append=True)
                await page.reload()
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                result = await page.evaluate("document.getElementsByClassName(\"tlid-translation\")[0].innerText")
            if debug:
                write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Setting last_translation global variable to new translation...\n', append=True)
            last_translation = str(result)
            if cache:
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Adding result to cache...\n', append=True)
                add_translation_cache(source_language=source_language, destination_language=destination_language, source=text, result=str(result))
            if debug:
                write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Returning value... {result}\n', append=True)
            return str(result)
        except ElementHandleError:
            if debug:
                write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Element not found on page...\n', append=True)
            try:
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] New attempt...\n', append=True)
                await page.goto(f"https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}")
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                result = await page.evaluate("document.getElementsByClassName(\"tlid-translation\")[0].innerText")
                if result == last_translation or result == str(last_translation + '...'):
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Translation not finished detected... Refreshing page before new attempt...\n', append=True)
                    await page.reload()
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                    result = await page.evaluate("document.getElementsByClassName(\"tlid-translation\")[0].innerText")
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Setting last_translation global variable to new translation...\n', append=True)
                last_translation = str(result)
                if cache:
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Adding result to cache...\n', append=True)
                    add_translation_cache(source_language=source_language, destination_language=destination_language, source=text, result=str(result))
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Returning value... {result}\n', append=True)
                return str(result)
            except ElementHandleError:
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Element not found on page...\n', append=True)
                try:
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] New attempt...\n', append=True)
                    await page.goto(f"https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}")
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Translation not finished detected... Refreshing page before new attempt...\n', append=True)
                    await page.reload()
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                    result = await page.evaluate("document.getElementsByClassName(\"tlid-translation\")[0].innerText")
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Setting last_translation global variable to new translation...\n', append=True)
                    last_translation = str(result)
                    if cache:
                        if debug:
                            write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Adding result to cache...\n', append=True)
                        add_translation_cache(source_language=source_language, destination_language=destination_language, source=text, result=str(result))
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 3] Returning value... {result}\n', append=True)
                    return str(result)
                except ElementHandleError:
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
                await page.goto(f"https://{gt_domain}/?hl=en#view=home&op=translate&sl={verify_language_code(source_language)}&tl={verify_language_code(destination_language)}&text={str(text)}")
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                result = await page.evaluate("document.getElementsByClassName(\"tlid-translation\")[0].innerText")
                if result == last_translation or result == str(last_translation + '...'):
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Translation not finished detected... Refreshing page before new attempt...\n', append=True)
                    await page.reload()
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Getting DOM Element by Class Name (tlid-translation)\n', append=True)
                    result = await page.evaluate("document.getElementsByClassName(\"tlid-translation\")[0].innerText")
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Setting last_translation global variable to new translation...\n', append=True)
                last_translation = str(result)
                if cache:
                    if debug:
                        write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Adding result to cache...\n', append=True)
                    add_translation_cache(source_language=source_language, destination_language=destination_language, source=text, result=str(result))
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - [Attempt 2] Returning value... {result}\n', append=True)
                return str(result)
            except Exception as e:
                if debug:
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Unknown error\n', append=True)
                    write_file('logs.txt', today() + ' ' + current_time() + f'   text={text}｜sl={source_language}｜dl={destination_language} - Error details: {str(e)}\n', append=True)
                return "An error occured while translating: unknown error."

def translate(text, destination_language, source_language="auto", cache=False, debug=False):
    """
    Translates the given text into the chosen language by scraping Google Translate with Selenium.

    Returns a string with the text translated.\n
    Returns "An error occured while translating: translation not found." if the translation was not found in the webpage. This might come from a mistyped language code.
    """
    result = asyncio.get_event_loop().run_until_complete(_translate(text=text, destination_language=destination_language, source_language=source_language, cache=cache, debug=debug))
    return result





async def _detect_language(text, result_language='en'):
    """
    Internal Function for detect_language()
    """
    from .domain import gt_domain
    try:
        await page.goto(f"https://{gt_domain}/?hl={verify_language_code(result_language)}#view=home&op=translate&sl=auto&tl=en&text={str(text)}")
        await page.reload()
        raw_result = await page.evaluate("document.getElementsByClassName(\"jfk-button-checked\")[0].innerText")
        result = raw_result.split(' - ')[0]
        if result == 'Detect language':
            result = detect_language(text, result_language=result_language)
        return str(result)
    except:
        return "An error occured while detecting the language.\nPlease try again."
            
async def _transliterate(text, source_language="auto"):
    """
    Internal Function for transliterate()
    """
    from .domain import gt_domain
    try:
        await page.goto(f'https://{gt_domain}/#view=home&op=translate&sl={verify_language_code(source_language)}&tl=en&text={str(text)}')
        await page.reload()
        result = await page.evaluate("document.getElementsByClassName(\"tlid-transliteration-content\")[0].innerText")
        return str(result)
    except:
        return 'not available'

async def _definition(text, source_language="auto"):
    """
    Internal Function for definition()
    """
    from .domain import gt_domain
    await page.goto(f'https://{gt_domain}/#view=home&op=translate&sl={verify_language_code(source_language)}&tl=en&text={str(text)}')
    await page.reload()
    final_dict = {}
    try:
        word_type = await page.evaluate("document.getElementsByClassName(\"gt-cd-pos\")[0].innerText")
    except:
        word_type = 'not available.'
    try:
        word_definition = await page.evaluate("document.getElementsByClassName(\"gt-def-row\")[0].innerText")
    except:
        word_definition = 'not available.'
    try:
        example = await page.evaluate("document.getElementsByClassName(\"gt-def-example\")[0].innerText")
    except:
        example = 'not available.'
    final_dict['word_type'] = str(word_type)
    final_dict['definition'] = str(word_definition)
    final_dict['example'] = str(example)
    return final_dict



def detect_language(text, result_language='en'):
    """
    Returns the language of the given text.
    """
    result = asyncio.get_event_loop().run_until_complete(_detect_language(text=text, result_language=result_language))
    return result

def transliterate(text, source_language="auto"):
    """
    Returns the transliteration provided by Google Translate (if available)\n
    i.e Ohayou --> おはよう / おはよう --> Ohayou
    """
    result = asyncio.get_event_loop().run_until_complete(_transliterate(text=text, source_language=source_language))
    return result

def definition(text, source_language="auto"):
    """
    Returns the word type (i.e Interjection, Noun), defintion (if available) and sentence example where the word could be used (if available)
    """
    result = asyncio.get_event_loop().run_until_complete(_definition(text=text, source_language=source_language))
    return result
