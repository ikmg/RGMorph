from rg_morph import Text

texts = [
    'филиал федерального государственного казенного учреждения "Управление вневедомственной охраны по г. Балашиха Московской области" Центрального округа войск национальной гвардии Российской Федерации',
    'почетное звание "Почетный сотрудник Росгвардии"'
]

for item in texts:
    text = Text(item)
    for case in text.cases:
        print('Падеж <{}>:'.format(case))
        print('  игнорировать кавычки {}:'.format(True), text.morph(case, True))
        print('  игнорировать кавычки {}:'.format(False), text.morph(case, False))
