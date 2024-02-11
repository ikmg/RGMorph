from rg_morph import FIO


words = {
    'lastname': 'Кудрявцев',
    'firstname': 'Михаил',
    'middlename': 'Георгиевич',
    '123': 123
}

# words = {
#     'lastname': '',
#     'firstname': '',
#     'middlename': ''
# }

fio = FIO(**words)
print(words)
for case in fio.cases:
    print('Падеж <{}>'.format(case))
    print('  в строку {}:'.format(True), fio.morph('родительный', True))
    print('  в строку {}:'.format(False), fio.morph('родительный', False))
