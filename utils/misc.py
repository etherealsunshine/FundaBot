from io import StringIO
from html.parser import HTMLParser


LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}

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

LANGUAGES.values()

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def check_language(lang_input):
    if lang_input in list(TRANSLATION_LANGUAGES.keys()):
        return True
    else:
        return False
    
def get_language_code(lang_input):
    return TRANSLATION_LANGUAGES[lang_input]

def get_languages():
    return list(TRANSLATION_LANGUAGES.keys())


def check_number(input):
    try:
        int(input)
        return True
    except ValueError:
        try:
            float(input)
            return True
        except ValueError:
            return False


def is_zero(input):
    return input == 0
