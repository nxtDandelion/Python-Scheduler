import unittest
from unittest.mock import patch
from scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """Тестовые данные"""
        self.test_data = {
            "days": [
                {"id": 1, "date": "2025-02-15", "start": "09:00", "end": "21:00"},
                {"id": 2, "date": "2025-02-16", "start": "08:00", "end": "22:00"}
            ],
            "timeslots": [
                {"id": 1, "day_id": 1, "start": "17:30", "end": "20:00"},
                {"id": 2, "day_id": 1, "start": "09:00", "end": "12:00"},
                {"id": 3, "day_id": 2, "start": "14:30", "end": "18:00"}
            ]
        }

    def setUp(self):
        """Создаем экземпляр Scheduler для каждого теста"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = self.test_data
            self.scheduler = Scheduler(url="http://test.url")

    def test_get_busy_slots(self):
        """Тест получения занятых слотов"""
        busy_slots = self.scheduler.get_busy_slots("2025-02-15")
        self.assertEqual(len(busy_slots), 2)
        self.assertEqual(busy_slots[0], ("09:00", "12:00"))
        self.assertEqual(busy_slots[1], ("17:30", "20:00"))

    def test_get_free_slots(self):
        """Тест получения свободных слотов"""
        free_slots = self.scheduler.get_free_slots("2025-02-15")
        self.assertEqual(len(free_slots), 2)
        self.assertEqual(free_slots[0], ("12:00", "17:30"))
        self.assertEqual(free_slots[1], ("20:00", "21:00"))

    def test_is_available(self):
        """Тест проверки доступности слота"""
        self.assertTrue(self.scheduler.is_available("2025-02-15", "12:30", "13:00"))
        self.assertFalse(self.scheduler.is_available("2025-02-15", "11:00", "13:00"))

    def test_find_slot_for_duration(self):
        """Тест поиска слота по продолжительности"""
        slot = self.scheduler.find_slot_for_duration(90)  # 1.5 часа
        self.assertIsNotNone(slot)
        self.assertEqual(slot[0], "2025-02-15")

    def test_nonexistent_date(self):
        """Тест обработки несуществующей даты"""
        self.assertEqual(self.scheduler.get_busy_slots("2025-01-01"), [])
        self.assertEqual(self.scheduler.get_free_slots("2025-01-01"), [])


if __name__ == "__main__":
    unittest.main()
