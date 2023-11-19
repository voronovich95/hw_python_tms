
##### 1. Декодировать в строку байтовое значение: b'r\xc3\xa9sum\xc3\xa9'. Затем результат преодразовать в байтовый вид в кодировке ‘Latin1’ затем результат снова декодировать в строку (резултат всех преобразований выводить на экран)

```sh
first_str = b"r\xc3\xa9sum\xc3\xa9"
dec_str = first_str.decode('utf-8')
enc_str = dec_str.encode('latin1')
last_str = enc_str.decode('latin1')
print(first_str)
print(enc_str)
print(last_str)
```
##### 2. Ввести с клавиатуры 4 строки и сохранить их в разные 4 переменные. Создать файл и записать в него первые2 строки и закрыть файл. Затем открыть файл на редактирвоание и дозаписать оставшиеся 2 строки. В итоговом файле должны быть строки, каждая из которых должна начинаться с новой строки


```sh
str_1 = "Ввести с клавиатуры"
str_2 = "4 строки и сохранить"
str_3 = "их в разные 4 переменные"
str_4 = "Создать файл и записать "
with open('file_str.txt', 'w', encoding='utf-8') as file:
    file.write(f'{str_1}\n{str_2}\n')
with open('file_str.txt', 'a', encoding='utf-8') as file:
    file.write(f'{str_3}\n{str_4}\n')
```

##### 3. Создать словарь в качестве ключа которого будет 6-ти значное число (id) а в качестве значений кортеж состоящий из двух элементов имя(str, возврост(int). Сделать около 5-6 элементов словаряЗаписать данный словарь на диск в json файл.


```sh
import json
dict_1 = {111112: ("roman", 28),
          111113: ("darya", 27),
          111114: ("tima", 5),
          111115: ("olivia", 1),
          111116: ("toma", 48)}
with open('file_json.json', 'w') as file:
    json.dump(dict_1, file, indent=2, ensure_ascii=False)
```
##### 4. Прочитать сохраненный json-файл и записать данные на диск в csv-файл, первой строкой которого озоглавив первый столбец и добавив новый столбец "телефон"
```sh
import json
import csv

with open('file_json.json', 'r') as file_json:
    data_json = json.load(file_json)

with open('data.csv', 'w') as file_csv:
    name_colum = ['id', 'name', 'age', 'phone']
    numbers = ['111-111', '222-222', '333-333', '555-555', '666-666']
    data_csv = csv.DictWriter(file_csv, fieldnames=name_colum)
    data_csv.writeheader()
    for i, j in zip(data_json, numbers):
        data_csv.writerow({'id': i, 'name': data_json[i][0], 'age': data_json[i][1], 'phone': j})

with open('data.csv', 'r') as file_csv:
    data_csv_read = csv.reader(file_csv)
    for i in data_csv_read:
        print(i)

```
##### 5. Прочитать сохранённый csv-файл и сохранить данные в excel-файле, кроме возраста - столбец с этими данными не нужен. Таблица должна выглядить, как на примере.

```sh
import csv
import openpyxl

with open('data.csv', 'r') as file_csv:
    data_csv = csv.DictReader(file_csv)

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    for i, dct in enumerate(data_csv):
        print(dct)
        del dct['age']
        if i == 0:
            worksheet.append(list(dct.keys()))
        worksheet.append(list(dct.values()))
    workbook.save('data.xlsx')
```