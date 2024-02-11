import os

import pymorphy2
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender


def _string_to_words(string):
    """Clear string.\n
    Return words list."""
    string = string.strip()
    while string.find('  ') >= 0:
        string = string.replace('  ', ' ')
    words_list = string.split(' ')
    return words_list


def _parsing_words(words_list):
    """Parsing words in list.\n
    Return all variants of morphing."""
    morph = pymorphy2.MorphAnalyzer()
    parsed_words = []
    for word in words_list:
        parsed_word = morph.parse(word)
        parsed_words.append(parsed_word)
    return parsed_words


def _catch_variant(variants):
    """Catch needs tags kit in word morph variants.\n
    Return one variant or None.\n
    Tags matching OpenCorpora tags: http://opencorpora.org/dict.php?act=gram"""
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


class _Person:
    gender = None
    # before morphing
    lastname = None
    firstname = None
    middlename = None
    # after morphing
    cased_lastname = None
    cased_firstname = None
    cased_middlename = None


class Morph:
    """USING:\n
    method <phrase(case, str)> - for casing any string except fio;\n
    method <fio(case, **kwargs)> - for casing fio;\n
    property <info> - show full info about last operation in all cases.\n\n
    PRINTS:\n
    print(morph) - show details of last operation or view in debug mode\n
    print(morph.info) - show full info about last operation in all cases\n
    print(morph.phrase(*args)) - show result\n
    print(morph.fio(*args, **kwargs)) - show result
    """

    # dictionary of cases by:
    # pymorphy2 - list[0], also match OpenCorpora;
    # petrovich - list[1].
    _genetive_dict = {
        'именительный': ['nomn', None],
        'родительный': ['gent', Case.GENITIVE],
        'дательный': ['datv', Case.DATIVE],
        'винительный': ['accs', Case.ACCUSATIVE],
        'творительный': ['ablt', Case.INSTRUMENTAL],
        'предложный': ['loct', Case.PREPOSITIONAL]
    }

    # PRIVATE

    def __init__(self):
        self._type = None  # type of operation
        self._case = None  # case name
        self._original_string = None  # input string
        self._original_words_list = None  # input words list
        self._parsed_words_list = None  # parsed words list
        self._cased_words_list = None  # cased words list
        self._cased_string = None  # cased string
        self._person = None  # person attributes for petrovich

    def _reset(self):
        self._type = None
        self._case = None
        self._original_string = ''
        self._original_words_list = []
        self._parsed_words_list = []
        self._cased_words_list = []
        self._cased_string = ''
        self._person = _Person()

    def __str__(self):
        result = 'Падеж: <{}>, '.format(self._case)

        if self._type == 'phrase':
            result = '{}входящая строка: <{}>, '.format(result, self._original_string)
        elif self._type == 'fio':
            result = '{}входящая строка: <{} {} {}>, '.format(result, self._person.lastname, self._person.firstname, self._person.middlename)

        if self._case == 'именительный':
            result = '{}именительный падеж (кто/что): <есть'.format(result)
        elif self._case == 'родительный':
            result = '{}родительный падеж (кого/чего): <нет'.format(result)
        elif self._case == 'дательный':
            result = '{}дательный падеж (кому/чему): <рад'.format(result)
        elif self._case == 'винительный':
            result = '{}винительный падеж (кого/что): <вижу'.format(result)
        elif self._case == 'творительный':
            result = '{}творительный падеж (кем/чем): <горжусь'.format(result)
        elif self._case == 'предложный':
            result = '{}предложный падеж (о ком/о чем): <мечтаю о/об'.format(result)

        if self._type == 'phrase':
            result = '{} {}>'.format(result, self._cased_string)
        elif self._type == 'fio':
            result = '{} {} {} {}>'.format(result, self._person.cased_lastname, self._person.cased_firstname, self._person.cased_middlename)
        return result

    # PROTECTED

    def _inflect(self, variant, index: int):
        """Morphing word. Return cased word."""
        old_word = self._original_words_list[index]
        new_word = variant.inflect({self._genetive_dict[self._case][0]}).word
        for index, letter in enumerate(old_word):
            if old_word[index].isupper():
                new_word = ''.join([new_word[:index], new_word[index].upper(), new_word[index+1:]])
        return new_word

    # PUBLIC

    def phrase(self, case: str, text: str) -> str:
        """Using example:\n
        morph.phrase('родительный', 'какая-то строка').\n
        Return cased string."""
        
        if not text:
            return text

        self._reset()
        self._type = 'phrase'
        self._case = case
        self._original_string = text
        self._original_words_list = _string_to_words(self._original_string)
        self._parsed_words_list = _parsing_words(self._original_words_list)
        for index, word in enumerate(self._parsed_words_list):
            cased_word = self._original_words_list[index]
            variant = _catch_variant(word)
            if variant:
                cased_word = self._inflect(variant, index)
            self._cased_words_list.append(cased_word)
        self._cased_string = ' '.join(self._cased_words_list)
        return self._cased_string

    def fio(self, case: str, **kwargs):
        """Using example:\n
        morph.fio('родительный', lastname='any', firstname='any', middlename='any', gender='male/female', to_string=True, upper=True)\n
        Return dictionary {'lastname': str | None, 'firstname': str | None, 'middlename': str | None}"""
        self._reset()
        self._type = 'fio'
        self._case = case
        path_rules = f'{os.path.dirname(os.path.abspath(__file__))}/rules.json'
        petrovich = Petrovich(rules_path=path_rules)
        if 'gender' in kwargs:
            self._person.gender = Gender.MALE if kwargs['gender'] == 'male' else Gender.FEMALE if kwargs['gender'] == 'female' else None
        if 'lastname' in kwargs:
            self._person.lastname = kwargs['lastname']
            self._person.cased_lastname = self._person.lastname
        if 'firstname' in kwargs:
            self._person.firstname = kwargs['firstname']
            self._person.cased_firstname = self._person.firstname
        if 'middlename' in kwargs:
            self._person.middlename = kwargs['middlename']
            self._person.cased_middlename = self._person.middlename

        if case != 'именительный':
            if self._person.lastname:
                self._person.cased_lastname = petrovich.lastname(self._person.lastname, self._genetive_dict[self._case][1], self._person.gender)
            if self._person.firstname:
                self._person.cased_firstname = petrovich.firstname(self._person.firstname, self._genetive_dict[self._case][1], self._person.gender)
            if self._person.middlename:
                self._person.cased_middlename = petrovich.middlename(self._person.middlename, self._genetive_dict[self._case][1], self._person.gender)

        if 'upper' in kwargs:
            if kwargs['upper'] and self._person.cased_lastname:
                self._person.cased_lastname = self._person.cased_lastname.upper()

        if 'to_string' in kwargs:
            if kwargs['to_string']:
                return ' '.join([
                    self._person.cased_lastname if self._person.cased_lastname else '',
                    self._person.cased_firstname if self._person.cased_firstname else '',
                    self._person.cased_middlename if self._person.cased_middlename else ''
                ]).strip()
            else:
                return self.result
        else:
            return self.result

    @property
    def result(self):
        return {
            'lastname': self._person.cased_lastname,
            'firstname': self._person.cased_firstname,
            'middlename': self._person.cased_middlename
        }

    @property
    def info(self) -> str:
        """Full info about last operation"""
        result = None
        if self._type == 'phrase':
            result = 'Входящая строка: {}\n'.format(self._original_string)
            result = '{}Именительный падеж (кто/что): есть {}\n'.format(result, self.phrase('именительный', self._original_string))
            result = '{}Родительный падеж (кого/чего): нет {}\n'.format(result, self.phrase('родительный', self._original_string))
            result = '{}Дательный падеж (кому/чему): рад {}\n'.format(result, self.phrase('дательный', self._original_string))
            result = '{}Винительный падеж (кого/что): вижу {}\n'.format(result, self.phrase('винительный', self._original_string))
            result = '{}Творительный падеж (кем/чем): горжусь {}\n'.format(result, self.phrase('творительный', self._original_string))
            result = '{}Предложный падеж (о ком/о чем): мечтаю о/об {}\n'.format(result, self.phrase('предложный', self._original_string))
            result = '{}Морфологический разбор слов входящей строки:\n'.format(result)
            for word in self._parsed_words_list:
                result = '{}- слово [{}]\n'.format(result, word[0].word)
                for variant in word:
                    result = '{}  {}\n'.format(result, variant)
        elif self._type == 'fio':
            result = 'Входящая строка: {} {} {}\n'.format(self._person.lastname, self._person.firstname, self._person.middlename)
            fio = self.fio('именительный', lastname=self._person.lastname, firstname=self._person.firstname, middlename=self._person.middlename, gender=self._person.gender)
            result = '{}Именительный падеж (кто/что): есть {} {} {}\n'.format(result, fio['lastname'], fio['firstname'], fio['middlename'])
            fio = self.fio('родительный', lastname=self._person.lastname, firstname=self._person.firstname, middlename=self._person.middlename, gender=self._person.gender)
            result = '{}Родительный падеж (кого/чего): нет {} {} {}\n'.format(result, fio['lastname'], fio['firstname'], fio['middlename'])
            fio = self.fio('дательный', lastname=self._person.lastname, firstname=self._person.firstname, middlename=self._person.middlename, gender=self._person.gender)
            result = '{}Дательный падеж (кому/чему): рад {} {} {}\n'.format(result, fio['lastname'], fio['firstname'], fio['middlename'])
            fio = self.fio('винительный', lastname=self._person.lastname, firstname=self._person.firstname, middlename=self._person.middlename, gender=self._person.gender)
            result = '{}Винительный падеж (кого/что): вижу {} {} {}\n'.format(result, fio['lastname'], fio['firstname'], fio['middlename'])
            fio = self.fio('творительный', lastname=self._person.lastname, firstname=self._person.firstname, middlename=self._person.middlename, gender=self._person.gender)
            result = '{}Творительный падеж (кем/чем): горжусь {} {} {}\n'.format(result, fio['lastname'], fio['firstname'], fio['middlename'])
            fio = self.fio('предложный', lastname=self._person.lastname, firstname=self._person.firstname, middlename=self._person.middlename, gender=self._person.gender)
            result = '{}Предложный падеж (о ком/о чем): мечтаю о/об {} {} {}\n'.format(result, fio['lastname'], fio['firstname'], fio['middlename'])
        return result
