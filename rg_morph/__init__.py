from .fio import FIO
from .text import Text


class Morph:
    """
    Класс для обратной совместимости с предыдущей версией
    """

    def __init__(self):
        self.text = None
        self.person = None

    def fio(self, case: str, **keywords):
        """
        Склонение ФИО.
        param: case: str - наименование падежа из словаря cases
        **keywords: все необязательные, но все не могут быть пустыми
        param: lastname: str - фамилия
        param: firstname: str - имя
        param: middlename: str - отчество
        param: gender: str (male/female) - пол
        param: to_string: bool - результат склонения конкатенирует в строку
        """
        self.person = FIO(
            lastname=keywords['lastname'] if 'lastname' in keywords else None,
            firstname=keywords['firstname'] if 'firstname' in keywords else None,
            middlename=keywords['middlename'] if 'middlename' in keywords else None,
            gender=keywords['gender'] if 'gender' in keywords else None
        )
        return self.person.morph(case, keywords['to_string'] if 'to_string' in keywords else False)

    def phrase(self, case: str, text: str, ignore_text_in_quotes: bool = False):
        """
        Изменение склонения текста.
        param: case: str - наименование падежа из словаря cases
        param: text: str - текст для изменения склонения
        param: ignore_text_in_quotes: bool - игнорировать (не склонять) текст в кавычках
        """
        self.text = Text(text)
        return self.text.morph(case, ignore_text_in_quotes)
