from rg_morph import Text

text = Text('это "текст для" изменения склонения')

print(text.morph('родительный', True))
print(text.morph('предложный', False))
