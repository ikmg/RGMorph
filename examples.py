from rg_morph import FIO, Text, Morph


# Пример использования класса FIO

person = {
    'lastname': 'Иванов',
    'firstname': 'Иван',
    'middlename': 'Иванович',
    'gender': 'male'
}

fio = FIO(**person)
print(fio.morph('родительный', True))
print(fio.morph('предложный', False))

# Пример использования класса Text

text = Text('это "текст для" изменения склонения')

print(text.morph('родительный', True))
print(text.morph('предложный', False))

# Пример использования класса Morph

person_item = {
    'lastname': 'Иванов',
    'firstname': 'Иван',
    'middlename': 'Иванович',
    'gender': 'male',
    'rank': 'рядовой',
    'post': 'стрелок 1 взвода 1 роты',
    'unit': '1 батальон охраны',
    'subject': 'федеральное государственное казенное учреждение "Префектура ЮВАО г. Москва"'
}

employee = Morph(**person_item)
print(employee.fio.morph('родительный', True))
print(employee.rank.morph('родительный', True))
print(employee.post.morph('родительный', True))
print(employee.unit.morph('родительный', True))
print(employee.subject.morph('родительный', True))
