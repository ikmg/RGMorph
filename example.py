from old_morph import Morph


morph = Morph()

# morph phrase example

res = morph.phrase('родительный', 'ФГКУ "Главный центр Оршанско-Хинганский Федерации"')
print('morph.phrase(case, text) result: <{}>'.format(res))
print('-'*50)

# morph fio example

res = morph.fio('родительный', lastname='Казанцев', firstname='Георгий', middlename='Валентинович', gender='male')
print('morph.fio(case, **kwargs) result: <{}>'.format(res))
print('-'*50)

res = morph.fio('родительный', lastname='Казанцев', firstname='Георгий', middlename='Валентинович', gender='male', to_string=True, upper=True)
print('morph.fio(case, **kwargs) result: <{}>'.format(res))
print('-'*50)
