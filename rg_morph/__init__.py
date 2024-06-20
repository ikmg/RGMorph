from .fio import FIO
from .text import Text


class Morph:
    """
    Класс сведений о персоне и ее должностном положении
    """

    def __init__(self, **keywords):
        self.fio = FIO(
            lastname=keywords['lastname'] if 'lastname' in keywords else '',
            firstname=keywords['firstname'] if 'firstname' in keywords else '',
            middlename=keywords['middlename'] if 'middlename' in keywords else '',
            gender=keywords['gender'] if 'gender' in keywords else None
        )
        self.rank = Text(keywords['rank']) if 'rank' in keywords else ''
        self.post = Text(keywords['post']) if 'post' in keywords else ''
        self.unit = Text(keywords['unit']) if 'unit' in keywords else ''
        self.subject = Text(keywords['subject']) if 'subject' in keywords else ''
        self.text = None

    def phrase(self, case: str, text: str, ignore_text_in_quotes: bool = True):
        """
        Изменение склонений слов в произвольном тексте
        (обратная совместимость с предыдущей версией)
        """
        self.text = Text(text)
        return self.text.morph(case, ignore_text_in_quotes)
