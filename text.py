import pymorphy2


def inspect(word):
    """Catch needs tags kit in word morph variants.\n
    Return one variant or None.\n
    Tags matching OpenCorpora tags: http://opencorpora.org/dict.php?act=gram"""
    variants = pymorphy2.MorphAnalyzer()
    variants = variants.parse(word)
    for index, variant in enumerate(variants):
        if 'NOUN' in variant.tag:
            if 'Surn' not in variant.tag and 'Name' not in variant.tag and 'Patr' not in variant.tag:
                if 'sing' in variant.tag and 'nomn' in variant.tag:
                    return variant
        elif 'ADJF' in variant.tag:
            if ('inan' in variant.tag and 'sing' in variant.tag and 'accs' in variant.tag) or \
                    ('neut' in variant.tag and 'sing' in variant.tag and 'accs' in variant.tag) or \
                    ('femn' in variant.tag and 'sing' in variant.tag and 'nomn' in variant.tag):
                return variant
        elif 'NUMR' in variant.tag and 'nomn' in variant.tag:
            return variant
    return None


def inflect(variant, case: str, word: str):
    """Morphing word. Return cased word."""
    result = variant.inflect(case).word
    for index, letter in enumerate(word):
        if word[index].isupper():
            result = ''.join([
                result[:index],
                result[index].upper(),
                result[index + 1:]
            ])
    return result


class Text:

    cases = {
        'именительный': 'nomn',
        'родительный': 'gent',
        'дательный': 'datv',
        'винительный': 'accs',
        'творительный': 'ablt',
        'предложный': 'loct'
    }

    def __init__(self, text: str):
        self.text = text
        self.words = self.splitter()

    def splitter(self):
        tmp = self.text
        while tmp.find('  ') >= 0:
            tmp = tmp.replace('  ', ' ')
        result = tmp.split(' ')
        return result

    def morph(self, case: str):
        if case not in self.cases:
            raise ValueError('неизвестный падеж <{}>'.format(case))

        result = []
        is_proper_next = True
        for index, word in enumerate(self.words):
            is_proper_curr = is_proper_next
            if '«' in word:
                is_proper_curr = False
                is_proper_next = False
            elif '»' in word:
                is_proper_curr = False
                is_proper_next = True
            if is_proper_curr:
                variant = inspect(self.words[index])
                if variant:
                    result.append(inflect(variant, self.cases[case], word))
                else:
                    result.append(word)
            else:
                result.append(word)

        return ' '.join(result)
