from rg_morph import FIO, Text, Morph


def test_fio(fio_dict: dict):
    fio = FIO(**fio_dict)
    print('FIO data: <{}>'.format(fio_dict))
    print('\tродительный - <{}>'.format(fio.morph(case='родительный', to_string=True)))
    print('\tпредложный - <{}>'.format(fio.morph(case='предложный', to_string=False)))


def test_text(text_value: str):
    text = Text(text_value)
    print('TEXT data: <{}>'.format(text_value))
    print('\tродительный with ignore - <{}>'.format(text.morph(case='родительный', ignore_text_in_quotes=True)))
    print('\tпредложный without ignore - <{}>'.format(text.morph(case='предложный', ignore_text_in_quotes=False)))


# Пример использования класса FIO
fio_dict = {}
test_fio(fio_dict)

fio_dict = {
    'lastname': 'Иванов',
    'firstname': 'Иван',
    'middlename': 'Иванович',
    'gender': 'male'
}
test_fio(fio_dict)

# Пример использования класса Text
text = ''
test_text(text)

text = 'это "текст для" изменения склонения'
test_text(text)

# Пример использования класса Morph

person_dict = {
    'lastname': 'Иванов',
    'firstname': 'Иван',
    'middlename': 'Иванович',
    'gender': 'male',
    'rank': 'рядовой',
    'post': 'стрелок 1 взвода 1 роты',
    'unit': '1 батальон охраны',
    'subject': 'федеральное государственное казенное учреждение "Префектура ЮВАО" г. Москва'
}

person = Morph(**person_dict)
print(person_dict)
print('\t', person.fio.morph(case='родительный', to_string=True))
print('\t', person.rank.morph(case='родительный', ignore_text_in_quotes=True))
print('\t', person.post.morph(case='родительный', ignore_text_in_quotes=True))
print('\t', person.unit.morph(case='родительный', ignore_text_in_quotes=True))
print('\t', person.subject.morph(case='родительный', ignore_text_in_quotes=True))
print('\t', person.phrase(case='родительный', text='какой-то случайный текст', ignore_text_in_quotes=False))
