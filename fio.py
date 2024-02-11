import os

from petrovich.main import Petrovich
from petrovich.enums import Case, Gender


class FIO:

    cases = {
        'родительный': Case.GENITIVE,
        'дательный': Case.DATIVE,
        'винительный': Case.ACCUSATIVE,
        'творительный': Case.INSTRUMENTAL,
        'предложный': Case.PREPOSITIONAL
    }

    def __init__(self, **keywords: str):
        # data
        self.lastname = keywords['lastname'] if 'lastname' in keywords else None
        self.firstname = keywords['firstname'] if 'firstname' in keywords else None
        self.middlename = keywords['middlename'] if 'middlename' in keywords else None
        self.gender = None
        if 'gender' in keywords:
            if keywords['gender'] == 'male':
                self.gender = Gender.MALE
            elif keywords['gender'] == 'female':
                self.gender = Gender.FEMALE
        # params
        self.rules = '{}/rules.json'.format(os.path.dirname(os.path.abspath(__file__)))
        # check
        if not self.lastname and not self.firstname and not self.middlename:
            raise ValueError('не указаны Фамилия, Имя и Отчество')

    def morph(self, case: str, to_string=False):
        petrovich = Petrovich(rules_path=self.rules)
        result = {
            'lastname': self.lastname,
            'firstname': self.firstname,
            'middlename': self.middlename
        }
        if case in self.cases:
            if self.lastname:
                result['lastname'] = petrovich.lastname(self.lastname, self.cases[case], self.gender)
            if self.firstname:
                result['firstname'] = petrovich.firstname(self.firstname, self.cases[case], self.gender)
            if self.middlename:
                result['middlename'] = petrovich.middlename(self.middlename, self.cases[case], self.gender)
        else:
            raise ValueError('неизвестный падеж <{}>, параметры необходимо указывать в именительном падеже'.format(case))

        if to_string:
            return '{} {} {}'.format(
                result['lastname'],
                result['firstname'],
                result['middlename']
            )
        else:
            return result
