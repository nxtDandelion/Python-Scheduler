# Python Scheduler

### Класс Scheduler работает с расписанием дней и слотов, позволяет узнавать занятые и свободные слоты, есть ли свободное время в определенный промежуток, узнать в какой день есть свободное время под определенную длительность.
### Методы:
```python
def load_data(self, url):
```
Выгружает данные по указанной ссылке. Так же обрабатывает возможные ошибки.

```python
def get_cleaned_data(self, data):
```
Преобразует "сырые" данные в удобные для последующей реализации функционала класса.

```python
def get_busy_slots(self, date):
```
Возвращает Вам список занятых промежутков в определенный день.

```python
def get_free_slots(self, date):
```
Возвращает Вам список свободных промежутков в определенный день.

```python
def is_available(self, date, start, end):
```
Проверяет, свободен ли промежуток в конкретную дату.

```python
def find_slot_for_duration(self, duration_minutes):
```
Возвращает Вам первый день с свободным слотом определенной длительности.

Так же в классе предусмотрена обработка некоторых ошибок.

Для проверки вам понадобится установка библиотеки requests. Установка возможна двумя вариантами:
1) Стандартная установка: 
```commandline
pip install requests
```
2) Установка с помощью файла requirements.txt:
```commandline
pip install -r requirements.txt
```

Пример использования:
```python
from scheduler import Scheduler

scheduler = Scheduler("https://ofc-test-01.tspb.su/test-task/")

busy = scheduler.get_busy_slots("2025-02-15")

free = scheduler.get_free_slots("2025-02-15")

available = scheduler.is_available("2025-02-15", "10:00", "11:00")

slot = scheduler.find_slot_for_duration(90)
```

Запуск тестов:
```commandline
python test.py
```


