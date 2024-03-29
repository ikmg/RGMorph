# RGMorph (изменение склонений)

Объединяет работу двух библиотек: 
- [pymorphy2](https://pymorphy2.readthedocs.io/en/stable/index.html)
- [petrovich](https://pypi.org/project/Petrovich/)

### Важно!

1. Не является универсальным средством. 
2. В качестве входных значений предполагается наличие слов в начальной форме (именительный падеж, единственное число). 
3. Работа настроена для использования при изменении склонений:
- _воинских (специальных) званий и(или) классных чинов, дипломатических рангов;_ 
- _фамилии, имени и(или) отчества;_
- _наименования должности, подразделения и(или) субъекта._

**Примечание:** _используется морфологический разбор слов основанный на тегах **[OpenCorpora](http://opencorpora.org/dict.php?act=gram)** и выбор подходящего варианта для изменения склонения._

### Особенности

При выявлении особых случаев, когда фамилия, имя или отчество склоняются неправильно, либо вообще не склоняются, они могут быть добавлены в набор правил (файл **rules.json**) в качестве исключений с явным указанием окончаний для каждого падежа. 

## Падежи
В методах классов используется аргумент **case**, для которого падежи указываются в привычной форме: 
- **именительный** - есть (кто/что), 
- **родительный** - нет (кого/чего), 
- **дательный** - рад (кому/чему), 
- **винительный** - вижу (кого/что), 
- **творительный** - горжусь (кем/чем), 
- **предложный** - мечтаю (о ком/о чем).

## Класс FIO

Используется отдельно для изменения склонений фамилии, имени и(или) отчества

### Инициализация
```
from rg_morph import FIO


person = {
    'lastname': 'Иванов',
    'firstname': 'Иван',
    'middlename': 'Иванович',
    'gender': 'male'
}

fio = FIO(**person)
```

### Изменение склонения

```
print(fio.morph('родительный', True))
>>> Иванова Ивана Ивановича

print(fio.morph('предложный', False))
>>> {'lastname': 'Иванове', 'firstname': 'Иване', 'middlename': 'Ивановиче'}
```

### Синтаксис

`fio.morph(case: str, to_string: bool = False)`
- param: **case**: str - _наименование падежа из словаря cases;_
- param: **to_string**: bool - _результат склонения ФИО конкатенирует в строку._

## Класс Text

Используется отдельно для изменения склонения воинских (специальных) званий и(или) классных чинов, 
дипломатических рангов, а также наименования должности, подразделения и(или) субъекта.


### Инициализация
```
from rg_morph import Text

text = Text('это "текст для" изменения склонения')
```

### Изменение склонения

```
print(text.morph('родительный', True))
>>> этого "текст для" изменения склонения

print(text.morph('предложный', False))
>>> этом "тексте для" изменения склонения
```

### Синтаксис

`text.morph(case: str, ignore_text_in_quotes: bool = False)`
- _param: **case**: str - наименование падежа для склонения;_
- _param: **ignore_text_in_quotes**: bool - игнорировать (не склонять) текст в кавычках._

## Класс Morph

Изменение склонений может также производиться объектом класса **Morph**. 

Класс **Morph** является инструментом для изменения склонений в установочных данных о персоне 
(ФИО, звание, должность, подразделение, субъект) чтобы использовать его в разных частях программы 
для изменения склонений одних и тех же данных.

### Инициализация

```
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

employee = Morph(**person_item)
```

Атрибуты:
- **.fio**: FIO - фамилия, имя, отчество, пол;
- **.rank**: Text - звание;
- **.post**: Text - должность;
- **.unit**: Text - подразделение;
- **.subject**: Text - субъект;
- **.text**: Text - резервный произвольный текст.

### Изменение склонения

Изменение склонений атрибутов класса **Morph** производится в соответствии с работой указанных классов.

Пример:
```
employee.fio.morph('родительный', True)
employee.rank.morph('дательный', False)
employee.subject.morph('винительный', True)
```

### Совместимость с предыдущей версией

Для совместимости с предыдущей версией в классе **Morph** существует метод **phrase**. 
Метод использует для работы атрибут .text.
