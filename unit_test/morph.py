from rg_morph import Morph


person_item = {
    'lastname': 'Фамилия',
    'firstname': 'Имя',
    'middlename': 'Отчество',
    'gender': 'male',
    'rank': 'рядовой',
    'post': 'стрелок 1 взвода 1 роты',
    'unit': '1 батальон охраны',
    'subject': 'войсковая часть 0000'
}

morph = Morph(**person_item)
q=1