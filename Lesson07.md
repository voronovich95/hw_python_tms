#### 1.Написать лямбда функцию определяющую чётное/нечётное. Функция принимает определяю определяющую чётное/нечётное. Функция принимает щую определяющую чётное/нечётное. Функция принимает чётное нечётное Функция принимаетпараметр число и если чётное то выдаёт слово “чётное”, если нет - то “нечётное”. если нет то “нечётное”

```sh
get_value = lambda x: "четное" if x % 2 == 0 else "нечетное"
print(get_value(8))
```

#### 2.Дан список чисел Вернуть список где при помощи функции map() каждое число каждое число переведено в строку В качестве функции в map() каждое число исползовать lambda map().

```sh
numbers = [1, 2, 3, 4, 5, 6]
result = map(lambda x: str(x), numbers)
print(list(result))
```

#### 3.ри помощи функции filter() из котрежа слов отфильтровать только те, которые из котрежа слов отфильтровать только те которые являю определяющую чётное/нечётное. Функция принимает тся полиндромами которые читаю определяющую чётное/нечётное. Функция принимает одинаково в обе стороны 
```sh
tuple_value = ('12321', 'python', 'force', 'шалаш', 'non')
def get_palindromes():
     for i in tuple_value:
         if i == i[::-1]:
             print(i)
get_palindromes()

result = filter(lambda x: x == x[::-1], tuple_value)
print(list(result))
```

#### 4.Написать декоратор к 2-м любым функциям который бы считал и выводил время бы считал и выводил время их выполнения. Подсказка: выполнения Подсказка map() . map() : from datetime import datetime time = datetime.now()

```sh
from datetime import datetime
tuple_value = ('12321', 'python', 'force', 'шалаш', 'non')
strint_value = '12321 python force шалаш non'

def get_time_working(func):
     def wrapper():
         start = datetime.now()
         func()
         end = datetime.now()
         print('Время выполнения: {} секунд.'.format(end - start))
     return wrapper

@get_time_working
def get_len_tuple():
     return len(tuple_value)
get_len_tuple()

@get_time_working
def get_tuple_from_string():
    new_string = tuple(strint_value.split())
    return new_string
get_tuple_from_string()
```

#### 5.Сделать функцию которая на вход принимает строку. Анализирует ее исключительно методом isdigit без доп библиотек и переводит строку. Функция умеет распознавать отрицательные числа и десятичные дроби 

```sh
def get_int_from_str(text):
    try:
        input_value = int(text)
        if input_value > 0:
            print("Вы ввели целое положительно число:", input_value)
        else:
            print("Вы ввели целое отрицательно число:", input_value)
    except:
        try:
            input_value = float(text)
            if input_value > 0:
                print("Вы ввели положительно дробное число:", input_value)
            else:
                print("Вы ввели отрицательное дробное число:", input_value)
        except:
            print("Вы ввели некорректное число")

get_int_from_str("-2.5")
```