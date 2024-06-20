import pymorphy2

from .config import pymorphy_cases


def _get_variant_(word):
    """
    Определение соответствия слова необходимым граммемам.
    При соответствии возвращает варианты морфологического разбора слова,
    при несоответствии возвращает None.
    Для морфологического разбора используются теги OpenCorpora:
    https://opencorpora.org/dict.php?act=gram
    param: word: str - слово
    """
    variants = pymorphy2.MorphAnalyzer()
    variants = variants.parse(word)  # морфологический разбор слова
    for index, variant in enumerate(variants):  # перебор вариантов морфологического разбора
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


def _get_cased_(variant, case: str, word: str):
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
            result = ''.join(
                [
                    result[:index],
                    result[index].upper(),
                    result[index + 1:]
                ]
            )
    return result


def _cutter_(text: str) -> list:
    """
    Разбивка текста на слова
    """
    tmp = text
    while tmp.find('  ') >= 0:
        tmp = tmp.replace('  ', ' ')
    result = tmp.split(' ')
    return result


class Text:
    """
    Склонение текста по падежам (кроме ФИО)
    param: text: текст со словами в именительном падеже
    """

    def __init__(self, text: str):
        self.text = text.strip()
        self.words = _cutter_(self.text)

    def morph(self, case: str, ignore_text_in_quotes: bool = True) -> str:
        """
        Изменение склонения текста.
        param: case: str - наименование падежа из словаря cases
        param: ignore_text_in_quotes: bool - игнорировать (не склонять) текст в кавычках
        """

        # исключение если падеж отсутствует в словаре
        if case not in pymorphy_cases:
            raise ValueError('Unknown case <{}>'.format(case))

        # результирующий список слов с измененным склонением
        result = []
        is_proper_curr = True  # необходимость склонения текущего слова по тексту
        is_proper_next = True  # необходимость склонения следующего слова по тексту

        # перебор слов
        for word in self.words:
            # игнорирование текста в кавычках
            if ignore_text_in_quotes:
                is_proper_curr = is_proper_next
                # если (открывается кавычка елочка) или (есть двойная кавычка и следующее слово подлежит склонению)
                if '«' in word or ('"' in word and is_proper_next):
                    is_proper_curr = False
                    is_proper_next = False
                # если (закрывается кавычка елочка) или (есть двойная кавычка и следующее слово не подлежит склонению)
                elif '»' in word or ('"' in word and not is_proper_next):
                    is_proper_curr = False
                    is_proper_next = True
            # склонение слова
            if is_proper_curr:
                variant = _get_variant_(word)
                if variant:
                    cased = _get_cased_(variant, pymorphy_cases[case], word)
                    result.append(cased)
                else:
                    result.append(word)
            else:
                result.append(word)

        # сборка результата в новый текст
        return ' '.join(result)
