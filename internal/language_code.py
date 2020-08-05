"""
Used to verify language codes/translate from language name to language code (i.e french --> fr)

© Anime no Sekai - 2020
"""

from . import google_translate_data

class LanguageCodeError(Exception):
    """
    When the language code is incorrect.
    """
    def __init__(self, msg=None):
        self.msg = msg 
    def __str__(self):
        exception_msg = f"\n\n⚠️ ⚠️ ⚠️\n{self.msg}\n"
        return exception_msg

def verify_language_code(language):
    """
    Verifies and gets the correct language code.
    """
    if language.lower() == 'zh-cn':
        return 'zh-CN'
    if language.lower() == 'zh-tw':
        return 'zh-TW'
    if language.lower() in google_translate_data.language_code_data():
        return language.lower()
    else:
        try:
            result = google_translate_data.language_name_to_code()[language.lower()]
            return result
        except:
            try:
                result = google_translate_data.international_language_name_to_code()[language.lower()]
                return result
            except:
                raise LanguageCodeError(f'{language} is not a correct language code.')
