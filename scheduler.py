import requests
from datetime import timedelta, datetime


class Scheduler:
    def __init__(self, url):
        self.data = self.load_data(url)

    def load_data(self, url):
        """Загрузка данных по ссылке"""
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return self.get_cleaned_data(response.json())
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка загрузки данных: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга JSON: {str(e)}")

    def get_cleaned_data(self, data):
        """Получение "чистых" данных для реализации функционала"""
        cleaned_data = {}
        for day in data["days"]:
            cleaned_data[day["date"]] = {
                'timeslots': [],
                'start': day['start'],
                'end': day['end']
            }
            for ts in data["timeslots"]:
                if day["id"] == ts["day_id"]:
                    cleaned_data[day["date"]]['timeslots'].append((ts['start'], ts['end']))
        return cleaned_data

    def get_busy_slots(self, date):
        """Получение занятых слотов определенного дня.
        Формат: YYYY-MM-DD"""
        if date not in self.data:
            return []
        return sorted(self.data[date]['timeslots'])

    def get_free_slots(self, date):
        """Получение свободных слотов определенного дня.
        Формат: YYYY-MM-DD"""
        if date not in self.data:
            return []
        day = self.data[date]
        slots = sorted(self.get_busy_slots(date))
        start, end = day['start'], day['end']
        free = []
        if slots:
            first = slots[0][0]
            if start < first:
                free.append((start, first))
        else:
            return [(start, end)]
        for i in range(1, len(slots)):
            temp_start = slots[i][0]
            prev_end = slots[i - 1][1]
            if prev_end < temp_start:
                free.append((prev_end, temp_start))
        if slots[-1][1] < end:
            free.append((slots[-1][1], end))
        return free

    def is_available(self, date, start, end):
        """Проверка, что есть свободное время для опрееделенного промежутка и дня.
        Формат: YYYY-MM-DD, HH-MM, HH-MM"""
        slots = self.get_free_slots(date)
        for slot_start, slot_end in slots:
            if slot_start <= start and slot_end >= end:
                return True
        return False

    def find_slot_for_duration(self, duration_minutes):
        """Поиск дня с свободным временем для определенной длительности.
        Формат: положительное число"""
        if not isinstance(duration_minutes, int) or duration_minutes <= 0:
            raise ValueError("duration_minutes должен быть положительным числом")
        duration = timedelta(minutes=duration_minutes)
        for date in sorted(self.data):
            free = self.get_free_slots(date)
            for slot_start, slot_end in free:
                start = datetime.strptime(f"{date} {slot_start}", "%Y-%m-%d %H:%M")
                end = datetime.strptime(f"{date} {slot_end}", "%Y-%m-%d %H:%M")
                if (end - start) >= duration:
                    end_result = (start + duration).strftime("%H:%M")
                    return date, slot_start, end_result
        return "Слот для подходящего времени не найден"


'''
scheduler = Scheduler(url="https://ofc-test-01.tspb.su/test-task/")
print(scheduler.get_busy_slots('2025-02-15'))
print(scheduler.get_free_slots('2025-02-15'))
print(scheduler.is_available('2025-02-15', '10:00', "10:30"))
print(scheduler.is_available('2025-02-15', '12:30', "13:00"))
print(scheduler.find_slot_for_duration(duration_minutes=60))
print(scheduler.find_slot_for_duration(duration_minutes=90))
'''
