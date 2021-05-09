TRANSLATION_LANGUAGES = {
    'afrikaans' : 'af',
    'albanian' : 'sq',
    'amharic' : 'am',
    'ar' : 'arabic',
    'armenian' : 'hy',
    'azerbaijani' : 'az',
    'basque' : 'eu',
    'bengali' : 'bn',
    'catalan' : 'ca',
    'chinese (simplified)' : 'zh-cn',
    'chinese (traditional)' : 'zh-dw',
    'croatian' : 'hr',
    'czech' : 'cs',
    'danish' : 'da',
    'english' : 'en',
    'esperanto' : 'eo',
    'filipino' : 'tl',
    'french' : 'fr',
    'german' : 'de',
    'greek' : 'el',
    'hebrew' : 'he',
    'hindi' : 'hi',
    'icelandic' : 'is',
    'indonesian' : 'id',
    'hungarian' : 'hu',
    'italian' : 'it',
    'japanese' : 'ja',
    'kazakh' : 'kk',
    'latvian' : 'lv',
    'malay' : 'ms',
    'norwegian' : 'no',
    'persian' : 'fa',
    'polish' : 'pl',
    'portuguese' : 'pt',
    'russian' : 'ru',
    'serbian' : 'sr',
    'spanish' : 'es',
    'swedish' : 'sv',
    'thai' : 'th',
    'vietnamese' : 'vi',
    'welsh' : 'cy'
}

def check_language(lang_input):
    if lang_input in list(TRANSLATION_LANGUAGES.keys()):
        return True
    else:
        return False
    
def get_language_code(lang_input):
    return TRANSLATION_LANGUAGES[lang_input]

def get_languages():
    return list(TRANSLATION_LANGUAGES.keys())