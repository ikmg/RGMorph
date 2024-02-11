from fio import FIO


# words = {
#     'lastname': 'Кудрявцев',
#     'firstname': 'Михаил',
#     'middlename': 'Георгиевич',
#     '123': 123
# }
#
# # words = {
# #     'lastname': '',
# #     'firstname': '',
# #     'middlename': ''
# # }
#
# fio = FIO(**words)
# # print(fio.morph('именительный'))
# print(fio.morph('родительный', True))
# print(fio.morph('дательный', True))
# print(fio.morph('винительный', True))
# print(fio.morph('творительный', True))
# print(fio.morph('предложный', True))


from text import Text

text = 'филиал федерального государственного казенного учреждения «Управление вневедомственной охраны по г. Балашиха Московской области» Центрального округа войск национальной гвардии Российской Федерации'

txt = Text(text)
print(txt.morph('именительный'))
print(txt.morph('родительный'))
print(txt.morph('дательный'))
print(txt.morph('винительный'))
print(txt.morph('творительный'))
print(txt.morph('предложный'))
q=1