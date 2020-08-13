# pyGoogleTranslate
 A python module for Google Translate (without using the API)

> It lets you use Google Translate (translation, transliteration, defintion, language detection, etc.) by parsing the website.

### This module lets you get four things:

- translate(text, destination_language, source_language)

Translates the given text into the chosen language.

    text: The text to translate
    destination_language: The language you want to get.
    source_language (default: auto): The language the text is in. ('auto' detects automatically the language the text is in)
    cache (default: False): Boolean value which determines if you want to cache the result in the translation cache file (to make the same translation or reverse translation faster the next time).
    debug (default: False): Boolean value which determines if you want to make a log file with what's happening when you run this function (useful to troubleshoot).

Returns a string.

- detect_language(text, result_language)

Gives the language of the given text.

    text: The text to check.
    result_language: The language of the output language.

Returns a string.

- transliterate(text, source_language)

Returns the transliteration provided by Google Translate (if available).

    text: The text to check.
    source_language (default: auto): The language the text is in.

Returns a string.

- definition(text, source_language)

Returns the word type (i.e Interjection, Noun), defintion (if available) and sentence example where the word could be used (if available)

    text: The text to check.
    source_language (default: auto): The language the text is in.

Returns a dictionnary.

### Other functions

- browser(browser_name, executable_path)

To choose the headless browser used by pyGoogleTranslate.

    browser_name: the name of the browser you want to use.
    executable_path (default: PATH): sets the executable path for your browser. 
    If executable_path is not changed, pyGoogleTranslate will consider that the browser driver/executable is in your PATH (for example if you downloaded the driver with Homebrew).

- browser_kill()

Kills the browser process in use.

    no argument to pass.

This needs to be call at the end of the execution of your program or when you plan to stop python because the browser will still be opened even if you shut down Python if you don't (which can results in multiple browsers opened even if you don't use them until you manually kills them in your activity monitor).


### Installation
You can install pyGoogleTranslate via `PIP` the Python Package Index Manager.

```bash
pip install pyGoogleTranslate
```

But you also need to install a compatible browser:
Browser | browser() command | Installation | Notes
------------ | ------------- | -------------- | --------------
PhantomJS | `pyGoogleTranslate.browser('phantomjs')` | On macOS with Homebrew `brew cask install phantomjs`  | PhantomJS is not maintained anymore but is the most lightweight of all three.  ⚠️It seems to not handle Japanese Characters well when rendering.
Firefox | `pyGoogleTranslate.browser('firefox')` | Install [Firefox](https://www.mozilla.org/en-US/firefox/new/) (with the name Firefox) and install the driver (on macOS with Homebrew `brew install geckodriver`) | I tested pyGoogleTranslate on Firefox and it seems to be quite long to start but works well with Japanese Characters which seemed to not work with PhantomJS. Seems to use lots of CPU when used multiple times in a row.
Chrome | `pyGoogleTranslate.browser('chrome')` | Install [Google Chrome](https://www.google.com/intl/en-US/chrome/) and install the driver (on macOS with Homebrew `brew cask install chromedriver`) | Same as Firefox but seems to use less CPU.


### Usage

```python
import pyGoogleTranslate
>>> pyGoogleTranslate.browser('<browser you want to use>')


>>> pyGoogleTranslate.translate('Hello', 'ja')
'こんにちは'

>>> pyGoogleTranslate.translate('Bonjour', source_language='french', destination_language='英語')
'Hello'

>>> pyGoogleTranslate.detect_language('Hola', 'es')
'español'

>>> pyGoogleTranslate.detect_language('Nihao', 'english')
'Chinese'

>>> pyGoogleTranslate.transliterate('Ohayou')
'おはよう'

>>> pyGoogleTranslate.transliterate('おはよう')
'Ohayou'

>>> pyGoogleTranslate.definition('おやすみ')
{'word_type': 'Noun', 'definition': '仕事などを休むこと。休暇。', 'example': '「一週間―をいただく」'}

>>> pyGoogleTranslate.detect_language('このPythonモジュールをダウンロード頂き誠にありがとうございました。')
'Japanese'

>>> pyGoogleTranslate.browser_kill()


```

### Notes

Data in `google_translate_data.py` are made by me except for the list of google translate domain names which I need to give credit to ssut in his project py-googletrans.

You can change the google translate domain with:

```python
>>> from pyGoogleTranslate.internal.domain import google_translate_domain
>>> google_translate_domain('<the new google translate domain>')
'<the new domain is returned>'
```

You can export your caches file with:
```python
>>> from pyGoogleTranslate.internal.caching import export_cache
>>> export_cache()

# The file is exported in the current directory
```

You can then import it with (for example after an update):
```python
>>> from pyGoogleTranslate.internal.caching import import_cache
>>> import_cache('<the path to the cache file>')

# The file is imported and merged with the current cache file
```

You can try using pyppeteer instead of Selenium with:

```python
>>> from pyGoogleTranslate.internal import pyGoogleTranslate_pyppeteer
>>> pyGoogleTranslate_pyppeteer.translate('Hello', 'japanese')
'こんにちは'

>>> pyGoogleTranslate_pyppeteer.detect_language('Hola', 'es')
'español'

>>> pyGoogleTranslate_pyppeteer.transliterate('Ohayou')
'おはよう'

>>> pyGoogleTranslate_pyppeteer.definition('おやすみ')
{'word_type': 'Noun', 'definition': '仕事などを休むこと。休暇。', 'example': '「一週間―をいただく」'}
```

You can try the new TTS Download function with:

```python
>>> from pyGoogleTranslate.internal.project.alpha.text_to_speech import text_to_speech
>>> text_to_speech('Hello', 'en', '1')

# The tts file is saved in your current directory
# Note that you need to install googletrans for this.
```

### Dependencies

This module has three python module dependency: [Selenium](https://www.selenium.dev/), [psutil](https://pypi.org/project/psutil/) and [lifeeasy](https://pypi.org/project/lifeeasy/) used to automate browsers which are downloaded when installing pyGoogleTranslate with PIP.


> Google Translate belongs to Google LLC, fully owned by Alphabet Inc.

> © Anime no Sekai - 2020
