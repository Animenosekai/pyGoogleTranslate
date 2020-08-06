from googletrans.gtoken import TokenAcquirer
from lifeeasy import request

def get_token(text):
    acquirer = TokenAcquirer()
    return acquirer.do(text)

def text_to_speech(text, language_code, tts_speed):
    token = get_token(text)
    response = request(f'https://translate.google.com/translate_tts?ie=UTF-8&q={str(text)}&tl={str(language_code)}&total=1&idx=0&textlen={str(len(text))}&tk={str(token)}&client=webapp&prev=input&ttsspeed={str(tts_speed)}')
    new_file = open(f'{text} - {language_code} (speed: {tts_speed}).mp3', 'wb')
    new_file.write(response.content)
    new_file.close()