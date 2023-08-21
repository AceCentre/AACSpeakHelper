import re

harf = '0-9٠-٩\u0620-\u064A\u066E-\u06D5\u06FA-\u06FF\u0750-\u077F'  # \u08A0-u08FF
haraka = '\u064B-\u065F'


def wordCount(text):
    t = re.findall('[' + harf + haraka + ']+', text)
    return len(t) if t else 0


def replaceByArray(text, array):
    if text:
        for i in range(0, len(array), 2):
            text = re.sub(array[i], array[i + 1], text, flags=re.IGNORECASE)
    return text


AliK = [
    'لاَ|لآ|لاً', 'ڵا',
    'لً|لَ|لأ', 'ڵ',
    'ة', 'ە',
    'ه' + '([^ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆەهھیێأإآثذصضطظكيىةڎۊؤ]|$)', 'هـ$1',
    'ض', 'چ',
    'ث', 'پ',
    'ظ', 'ڤ',
    'ط', 'گ',
    'ك', 'ک',
    'ىَ|يَ|یَ|آ', 'ێ',
    'رِ', 'ڕ',
    'ؤ|وَ', 'ۆ',
    'ي|ى', 'ی',
    'ء', '\u200Cو',
    'ِ', '',
    'ذ', 'ژ',
]
AliWeb = [
    'لاَ|لآ|لاً', 'ڵا',
    'لَ|پ', 'ڵ',
    'ة', 'ە',
    'ه', 'ھ',
    'ه', 'ھ',
    'رِ|أ', 'ڕ',
    'ؤ|وَ', 'ۆ',
    'يَ|یَ', 'ێ',
    'ص', 'ێ',
    'ي', 'ی',
    'ط', 'ڭ',
    'گ', 'ط',
    'ڭ', 'گ',
    'ض', 'چ',
    'ث', 'پ',
    'ظ', 'ڤ',
    'ْ|ُ', '',
    'ى', '*',
    'ك', 'ک',
    'ذ', 'ژ',
]
Dylan = [
    'لإ|لأ|لآ', 'ڵا',
    'ؤ|وَ', 'ۆ',
    'ة', 'ە',
    'ض', 'ڤ',
    'ص', 'ڵ',
    'ث', 'ێ',
    'ؤ', 'ۆ',
    'ه', 'ھ',
    'ك', 'ک',
    'ي|ى', 'ی',
    'ذ', 'ڕ',
]

ClearFormatting1 = [
    r'<!--(.*?)-->', '',  # comment
    r'[\r]+', '',
    r'[\n]+', ' ',
    r'(\\S)  (\\S)', r'$1 $2',
    r'&nbsp;', ' ',
    r'<img .+?>', '',
    r'</?o:p>', '',  # copy from MS Word
    r'<v:shapetype.*?>.*?<\/v:shapetype>', '',  # copy from MS Word
    r'<v:shape.*?>.*?<\/v:shape>', '',  # copy from MS Word
    r'<hr.*?>', '',
    r'<a.+?>(.*?)<\/a>', r'$1',
    r'<span[^>]*?>\\s*</\span>', '',
    r'<\/b>\\s*<b>', ''
]
ClearFormatting2 = [
    r'<([a-zA-Z1-9]+) .*?>', r'<$1>',
    r'<span id="menu".*?>([^<]*?)<\/span>', '',
    r'\u200C{2,}', '‌',  # zwnj
    r'<\/?pre.*?>', '‌',
    r'<span.*?>', '',
    r'<\/span>', '',
    r'<(p|h\\d)>', '<div>',
    r'<\/(p|h\\d)>', '</div>'
]


def clearFormatting(text):
    text = replaceByArray(text, ClearFormatting1)
    text = re.sub(r'<span[^>]+?font-family:[^>]*Ali_K_.+?>(.+?)<\/span>',
                  lambda match: replaceByArray(match.group(1), AliK), text)
    text = re.sub(r'<span[^>]+?font-family:[^>]*Ali_Web_.+?>(.+?)<\/span>',
                  lambda match: replaceByArray(match.group(1), AliWeb), text)
    text = re.sub(r'<span[^>]+?font-family:[^>]*Dylan.+?>(.+?)<\/span>',
                  lambda match: replaceByArray(match.group(1), Dylan), text)
    text = replaceByArray(text, ClearFormatting2).strip()
    text = NormalizeUnicode(text)
    text = InitialsFix(text)
    return text


def InitialsFix(text):
    text = re.sub(r'(^|[^' + harf + haraka + r'])ر([' + harf + haraka + r'])', r'\1ڕ\2', text)
    text = re.sub(r'(^|[^' + harf + haraka + r'])وو([' + harf + haraka + r'])', r'\1و\2', text)
    return text


CorrectionsNormalize = [
    'ي|ى|ے', 'ی',
    'یٔ', 'ئ',
    'ك|ڪ', 'ک',
    '[رڕ][ٍِ]', 'ڕ',
    '[ٍِ][رڕ]', 'ڕ',
    '[ًٌَُ][ی]', 'ێ',
    '[ی][ًٌَُ]', 'ێ',
    '[ًٌَُ][ڵل]', 'ڵ',
    '[ڵل][ًٌَُ]', 'ڵ',
    '[ًٌَُ][وۆؤ]', 'ۆ',
    '[وۆؤ][ًٌَُ]', 'ۆ',
    '\u200C{2,}', '\u200c',
    '\u06BE([^ـ' + harf + haraka + ']|$)', 'هـ$1',
    '\u06BE', 'ه',
    '\u0647\u200C', '\u06D5',
    '\u0647\u200D', 'هـ',
    '([ءادرڕزژوۆە])\u200C', '$1',
    '\u0647([^ـ' + harf + haraka + ']|$)', '\u06D5$1',
    '\u200Cو ', ' و ',
    '\u200C([^' + harf + ']|$)', '$1',
    '(^|[^' + harf + '])\u200C', '$1',
    'ـ{2,}', 'ـ',
    'ـ' + '([ئبپتجچحخسشعغفڤقکگلڵمنهیێءادرڕزژۆە])', '$1',
    '([بپتجچحخسشعغفڤقکگلڵمنیێ])' + 'ـ', '$1',
    '(^|[^هئ])' + 'ـ', '$1-'
]


def NormalizeUnicode(text):
    for pattern, replacement in zip(CorrectionsNormalize[::2], CorrectionsNormalize[1::2]):
        text = re.sub(pattern, replacement, text)
    return text


p1 = '[:؛؟!،,،]'
p2 = '[«\\(\\[]'
p3 = 'ی|یش|ش|ان|ەم|هەم|ەمین|هەمین|مان|تان|ەکە|ێک'
p4 = '[^ <>\\d\n\r"]'
p5 = '[\\)\\]»]'
regex_P = re.compile('(' +
                     '[\u003F,;"\u201C\u201D‐―–‒]|' +
                     '\\(\\(|' +
                     ' *\\)\\)|' +
                     '»[^\\)<>ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆەهھیێ :؛؟!،.،,]|' +
                     ' \\.|' +
                     r' *' + p1 + p4 + r'|' +
                     r' +' + p1 + p4 + r'?|' +
                     p4 + p2 + r' *|' +
                     p4 + r'?' + p2 + r' |' +
                     r'\d (' + p3 + r') |' +
                     r' +' + p5 + r'|' +
                     r' {3,}' +
                     ')', re.MULTILINE)


def InitialsFix(text):
    text = re.sub(r'(^|[^' + harf + haraka + r'])ر([' + harf + haraka + r'])', r'\1ڕ\2', text)
    text = re.sub(r'(^|[^' + harf + haraka + r'])وو([' + harf + haraka + r'])', r'\1و\2', text)
    return text


CorrectionsNormalize = [
    'ي|ى|ے', 'ی',
    'یٔ', 'ئ',
    'ك|ڪ', 'ک',
    '[رڕ][ٍِ]', 'ڕ',
    '[ٍِ][رڕ]', 'ڕ',
    '[ًٌَُ][ی]', 'ێ',
    '[ی][ًٌَُ]', 'ێ',
    '[ًٌَُ][ڵل]', 'ڵ',
    '[ڵل][ًٌَُ]', 'ڵ',
    '[ًٌَُ][وۆؤ]', 'ۆ',
    '[وۆؤ][ًٌَُ]', 'ۆ',
    '\u200C{2,}', '\u200c',
    '\u06BE([^ـ' + harf + haraka + ']|$)', 'هـ$1',
    '\u06BE', 'ه',
    '\u0647\u200C', '\u06D5',
    '\u0647\u200D', 'هـ',
    '([ءادرڕزژوۆە])\u200C', '$1',
    '\u0647([^ـ' + harf + haraka + ']|$)', '\u06D5$1',
    '\u200Cو ', ' و ',
    '\u200C([^' + harf + ']|$)', '$1',
    '(^|[^' + harf + '])\u200C', '$1',
    'ـ{2,}', 'ـ',
    'ـ' + '([ئبپتجچحخسشعغفڤقکگلڵمنهیێءادرڕزژۆە])', '$1',
    '([بپتجچحخسشعغفڤقکگلڵمنیێ])' + 'ـ', '$1',
    '(^|[^هئ])' + 'ـ', '$1-'
]


def NormalizeUnicode(text):
    for pattern, replacement in zip(CorrectionsNormalize[::2], CorrectionsNormalize[1::2]):
        text = re.sub(pattern, replacement, text)
    return text


p1 = '[:؛؟!،,،]'
p2 = '[«\\(\\[]'
p3 = 'ی|یش|ش|ان|ەم|هەم|ەمین|هەمین|مان|تان|ەکە|ێک'
p4 = '[^ <>\\d\n\r"]'
p5 = '[\\)\\]»]'
regex_P = re.compile('(' +
                     '[\u003F,;"\u201C\u201D‐―–‒]|' +
                     '\\(\\(|' +
                     ' *\\)\\)|' +
                     '»[^\\)<>ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆەهھیێ :؛؟!،.،,]|' +
                     ' \\.|' +
                     r' *' + p1 + p4 + r'|' +
                     r' +' + p1 + p4 + r'?|' +
                     p4 + p2 + r' *|' +
                     p4 + r'?' + p2 + r' |' +
                     r'\d (' + p3 + r') |' +
                     r' +' + p5 + r'|' +
                     r' {3,}' +
                     ')', re.MULTILINE)


def NormalizePunctuations(text):
    Corrections = [
        ('[‐―–‒]', '-'),  # -  ‐  ‑  ― – — ‒ _
        ('\u201C|\(\(', '«'),  # “ ((
        ('\u201D|\)\)', '»'),  # ” ))
        ('[\w' + harf + ']( +)[،:؛؟!)}\]»]( *)', r'\1\3 '),  # A )
        ('[،:؛؟!)}\]»]([\S])', r'\1 \2'),  # )A
        ('[،:؛؟!)}\]»] ([.،:؛؟!)}\]»])', r'\1\2'),  # ) ,
        ('\.([' + harf + ']{2,})', r'. \1'),  # .AB
        ('([' + harf + ']) \.', r'\1.'),  # AB .
        ('[«\[\({]( +)(\S+)', r'\1\3'),  # ( A
        ('(\S+)[«\[\({]', r'\1 \2'),  # A(
    ]
    for pattern, replacement in Corrections:
        text = re.sub(pattern, replacement, text)
    return text
