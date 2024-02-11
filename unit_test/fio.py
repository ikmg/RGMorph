from rg_morph import FIO


person = {
    'lastname': 'Иванов',
    'firstname': 'Иван',
    'middlename': 'Иванович',
    'gender': 'male'
}

fio = FIO(**person)
print(fio.morph('родительный', True))
print(fio.morph('предложный', False))
