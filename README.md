# pyGoogleTranslate
 A python module for Google Translate (without using the API)

### This module lets you get two things:

- translate(text, destination_language, source_language)

Translates the given text into the chosen language.

    text: The text to translate
    destination_language: The language code (two letters) of the language you want to get.
    source_language (default: auto): The language code (two letters) of the language the text is in. ('auto' detects automatically the language the text is in)

- detect_language(text, result_language)

Gives the language of the given text.

    text: The text to check.
    result_language: The language code (two letters) of the output language.

### Installation
You can install pyGoogleTranslate via `PIP` the Python Package Index Manager.

```bash
pip install pyGoogleTranslate
```

But you also need to install a compatible browser:
Browser | browser() command | Installation | Notes
------------ | ------------- | -------------- | --------------
PhantomJS | `pyGoogleTranslate.browser('phantomjs')` | On macOS with Homebrew `brew cask install phantomjs`  | PhantomJS is not maintained anymore but is the most lightweight of all three.  ⚠️It seems to not handle Japanese Characters well when rendering.
Firefox | `pyGoogleTranslate.browser('firefox')` | Install [Firefox](https://www.mozilla.org/en-US/firefox/new/) (with the name Firefox) and install the driver (on macOS with Homebrew `brew install geckodriver`) | I tested pyGoogleTranslate on Firefox and it seems to be quite long to start but works well with Japanese Characters which seemed to not work with PhantomJS
Chrome | `pyGoogleTranslate.browser('chrome')` | Install [Google Chrome](https://www.google.com/intl/en-US/chrome/) and install the driver (on macOS with Homebrew `brew cask install chromedriver`) | Same as Firefox.


### Usage

```python
import pyGoogleTranslate
>>> pyGoogleTranslate.browser('<browser you want to use>')


>>> pyGoogleTranslate.translate('Hello', 'ja')
'こんにちは'

>>> pyGoogleTranslate.translate('Bonjour', source_language='fr', destination_language='en')
'Hello'

>>> pyGoogleTranslate.detect_language('Hola')
'Spanish'

>>> pyGoogleTranslate.detect_language('Hola', 'es')
'español'

>>> pyGoogleTranslate.detect_language('Nihao')
'Chinese'

>>> pyGoogleTranslate.detect_language('このPythonモジュールをダウンロード頂き誠にありがとうございました。')
'Japanese'
```

### Dependencies

This module has one python module dependency: [Selenium](https://www.selenium.dev/), used to automate browsers which is downloaded when installing python-google-translate with PIP.


> Google Translate belongs to Google LLC, fully owned by Alphabet Inc.

> © Anime no Sekai - 2020