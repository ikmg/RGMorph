import os

from petrovich.main import Petrovich

from .config import petrovich_cases, petrovich_genders


class FIO:
    """
    Склонение ФИО.
    **keywords: все необязательные, но все не могут быть пустыми
    param: lastname: str - фамилия
    param: firstname: str - имя
    param: middlename: str - отчество
    param: gender: str (male/female) - пол
    """

    def __init__(self, **keywords: str):
        # скрытые атрибуты
        _ = os.path.dirname(os.path.abspath(__file__))
        self._rules_ = '{}/rules.json'.format(_)  # дополнительные правила склонения
        self._morpheus_ = Petrovich(rules_path=self._rules_)
        # данные
        self.lastname = keywords['lastname'] if 'lastname' in keywords else ''
        self.firstname = keywords['firstname'] if 'firstname' in keywords else ''
        self.middlename = keywords['middlename'] if 'middlename' in keywords else ''
        self.gender = petrovich_genders[keywords['gender']] if 'gender' in keywords else None

    def _morph_ln_(self, case: str) -> str:
        """Склонение фамилии"""
        return self._morpheus_.lastname(
            value=self.lastname.strip(),
            case=petrovich_cases[case],
            gender=self.gender
        ) if self.lastname else ''

    def _morph_fn_(self, case: str) -> str:
        """Склонение имени"""
        return self._morpheus_.firstname(
            value=self.firstname.strip(),
            case=petrovich_cases[case],
            gender=self.gender
        ) if self.firstname else ''

    def _morph_mn_(self, case: str) -> str:
        """Склонение отчества"""
        return self._morpheus_.middlename(
            value=self.middlename.strip(),
            case=petrovich_cases[case],
            gender=self.gender
        ) if self.middlename else ''

    def morph(self, case: str, to_string: bool = True):
        """
        Изменение склонения.
        param: case: str - падеж из словаря cases
        param: to_string: bool - результат склонения конкатенирует в строку
        """

        # исключение если падеж отсутствует в словаре
        if case not in petrovich_cases:
            raise ValueError('Unknown case <{}>'.format(case))

        # результирующий словарь
        result = {
            'lastname': self._morph_ln_(case),
            'firstname': self._morph_fn_(case),
            'middlename': self._morph_mn_(case)
        }

        # конкатенация результата
        return result if not to_string else '{}{}{}'.format(
                result['lastname'],
                ' {}'.format(result['firstname']) if result['firstname'] else result['firstname'],
                ' {}'.format(result['middlename']) if result['middlename'] else result['middlename']
            )
