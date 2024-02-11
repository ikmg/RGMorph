from .fio import FIO
from .text import Text


class Morph:
    """
    Класс сведений о персоне и ее должностном положении
    """

    def __init__(self, **keywords):
        self.fio = self.set_fio(**keywords)
        self.rank = Text(keywords['rank']) if 'rank' in keywords else None
        self.post = Text(keywords['post']) if 'post' in keywords else None
        self.unit = Text(keywords['unit']) if 'unit' in keywords else None
        self.subject = Text(keywords['subject']) if 'subject' in keywords else None
        self.text = None

    def set_fio(self, **keywords):
        """
        Установка сведений о персоне
        """
        return FIO(
            lastname=keywords['lastname'] if 'lastname' in keywords else None,
            firstname=keywords['firstname'] if 'firstname' in keywords else None,
            middlename=keywords['middlename'] if 'middlename' in keywords else None,
            gender=keywords['gender'] if 'gender' in keywords else None
        )

    def phrase(self, case: str, text: str, ignore_text_in_quotes: bool = False):
        """
        Изменение склонений слов в произвольном тексте
        (обратная совместимость с предыдущей версией)
        """
        self.text = Text(text)
        return self.text.morph(case, ignore_text_in_quotes)
