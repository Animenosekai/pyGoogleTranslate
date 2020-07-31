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
You can install python-google-translate via `PIP` the Python Package Index Manager.

```bash
pip install python-google-translate
```

But you also need to install [PhantomJS](https://phantomjs.org/download.html)

On macOS, you can install it with Homebrew:
```bash
brew cask install phantomjs
```


### Usage

```python
import pyGoogleTranslate

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

>>> pyGoogleTranslate.detect_language('Kono Python module wo daunrodo itadaki makoto ni arigatogozaimashita')
'Japanese'
```

### Dependencies

This module has one python module dependency: [Selenium](https://www.selenium.dev/), used to automate browsers which is downloaded when installing python-google-translate with PIP.

But you also need to install [PhantomJS](https://phantomjs.org/download.html), a headless, lightweight browser which I use to get webpages as quick as possible.



> Google Translate belongs to Google LLC, fully owned by Alphabet Inc.

> © Anime no Sekai - 2020