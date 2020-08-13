from internal import pyGoogleTranslate_pypeteer

print(pyGoogleTranslate_pypeteer.translate('Hello', 'japanese', debug=True))
print(pyGoogleTranslate_pypeteer.translate('おはよう', 'spanish', debug=True))
print(pyGoogleTranslate_pypeteer.transliterate('おはよう'))
print(pyGoogleTranslate_pypeteer.definition('Oyasumi'))
print(pyGoogleTranslate_pypeteer.detect_language('おはよう', 'japanese'))
print(pyGoogleTranslate_pypeteer.detect_language('Ohayou', 'french'))