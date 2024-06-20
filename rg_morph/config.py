from petrovich.enums import Case, Gender


# словарь с падежами и их классами для petrovich
petrovich_cases = {
    'родительный': Case.GENITIVE,
    'дательный': Case.DATIVE,
    'винительный': Case.ACCUSATIVE,
    'творительный': Case.INSTRUMENTAL,
    'предложный': Case.PREPOSITIONAL
}


# словарь с полами и их классами для petrovich
petrovich_genders = {
    'male': Gender.MALE,
    'female': Gender.FEMALE
}


# словарь с падежами для pymorphy и их обозначениями по тегам OpenCorpora
pymorphy_cases = {
    'родительный': 'gent',
    'дательный': 'datv',
    'винительный': 'accs',
    'творительный': 'ablt',
    'предложный': 'loct'
}
