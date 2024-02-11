import pymorphy2


def inspect(word):
    """
    Определение соответствия слова необходимым граммемам.
    При соответствии возвращает варианты морфологического разбора слова,
    при несоответствии возвращает None.
    Для морфологического разбора используются теги OpenCorpora:
    https://opencorpora.org/dict.php?act=gram
    param: word: str - слово
    """
    variants = pymorphy2.MorphAnalyzer()
    # морфологический разбор слова
    variants = variants.parse(word)
    # перебор вариантов морфологического разбора
    for index, variant in enumerate(variants):
        # имя существительное
        if 'NOUN' in variant.tag:
            # не фамилия, не имя и не отчество
            if 'Surn' not in variant.tag and 'Name' not in variant.tag and 'Patr' not in variant.tag:
                # единственное число и именительный падеж
                if 'sing' in variant.tag and 'nomn' in variant.tag:
                    return variant
        # имя прилагательное (полное)
        elif 'ADJF' in variant.tag:
            # (неодушевленное и единственное число и винительный падеж) или
            # (средний род и единственное число и винительный падеж) или
            # (женский род и единственное число и именительный падеж)
            if ('inan' in variant.tag and 'sing' in variant.tag and 'accs' in variant.tag) or \
                    ('neut' in variant.tag and 'sing' in variant.tag and 'accs' in variant.tag) or \
                    ('femn' in variant.tag and 'sing' in variant.tag and 'nomn' in variant.tag):
                return variant
        # числительное и именительный падеж
        elif 'NUMR' in variant.tag and 'nomn' in variant.tag:
            return variant
    return None


def inflect(variant, case: str, word: str):
    """
    Изменение склонения слова на основе представленного варианта морфологического разбора
    param: variant - вариант морфологического разбора слова
    param: case: str - наименование падежа из словаря cases
    param: word: str - слово
    """
    result = variant.inflect({case}).word
    # при изменении склонения все слова переводятся в нижний регистр
    # дальше производится обратная подстановка заглавных букв
    for index, letter in enumerate(word):
        if word[index].isupper():
            result = ''.join([
                result[:index],
                result[index].upper(),
                result[index + 1:]
            ])
    return result


class Text:
    """
    Склонение текста по падежам (кроме ФИО)
    param: text: текст со словами в именительном падеже
    """

    # словарь с падежами и их обозначениями по тегам OpenCorpora
    cases = {
        'именительный': 'nomn',
        'родительный': 'gent',
        'дательный': 'datv',
        'винительный': 'accs',
        'творительный': 'ablt',
        'предложный': 'loct'
    }

    def __init__(self, text: str):
        if not text:
            raise ValueError('текст не указан')
        self.text = text.strip()
        self.words = self.cutter()

    def cutter(self):
        """
        Разбивка текста на слова
        """
        tmp = self.text
        while tmp.find('  ') >= 0:
            tmp = tmp.replace('  ', ' ')
        result = tmp.split(' ')
        return result

    def morph(self, case: str, ignore_text_in_quotes: bool = False):
        """
        Изменение склонения текста.
        param: case: str - наименование падежа из словаря cases
        param: ignore_text_in_quotes: bool - игнорировать (не склонять) текст в кавычках
        """
        if case not in self.cases:
            raise ValueError('неизвестный падеж <{}>'.format(case))
        result = []
        is_proper_curr = True  # необходимость склонения текущего слова по тексту
        is_proper_next = True  # необходимость склонения следующего слова по тексту
        # перебор слов
        for index, word in enumerate(self.words):
            # игнорирование текста в кавычках
            if ignore_text_in_quotes:
                is_proper_curr = is_proper_next
                # если (открывается кавычка елочка) или (есть двойная кавычка и следующее слово подлежит склонению)
                if '«' in word or ('"' in word and is_proper_next == True):
                    is_proper_curr = False
                    is_proper_next = False
                # если (закрывается кавычка елочка) или (есть двойная кавычка и следующее слово не подлежит склонению)
                elif '»' in word or ('"' in word and is_proper_next == False):
                    is_proper_curr = False
                    is_proper_next = True
            # склонение слова
            if is_proper_curr:
                variant = inspect(self.words[index])
                if variant:
                    result.append(inflect(variant, self.cases[case], word))
                else:
                    result.append(word)
            else:
                result.append(word)
        # сборка результата в новый текст
        return ' '.join(result)
