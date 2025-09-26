from django.test import TestCase
from users.models import User
from habits.models import Habit


class HabitCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com',
                                        password='testpassword')

    def test_create_habit(self):
        habit_data = {
            'user': self.user,
            'place': 'Test Place',
            'action': 'Test Action',
            'period': 7,
            'reward': 'Test Reward',
            'max_time_processing': 100,
        }
        Habit.objects.create(**habit_data)
        self.assertEqual(Habit.objects.count(), 1)

    def test_read_habit(self):
        habit_data = {
            'user': self.user,
            'place': 'Test Place',
            'action': 'Test Action',
            'period': 7,
            'reward': 'Test Reward',
            'max_time_processing': 3600,
        }
        habit = Habit.objects.create(**habit_data)
        read_habit = Habit.objects.get(id=habit.id)
        self.assertEqual(read_habit.action, 'Test Action')

    def test_update_habit(self):
        habit_data = {
            'user': self.user,
            'place': 'Test Place',
            'action': 'Test Action',
            'period': 7,
            'reward': 'Test Reward',
            'max_time_processing': 3600,
        }
        habit = Habit.objects.create(**habit_data)
        habit.action = 'Updated Action'
        habit.save()
        updated_habit = Habit.objects.get(id=habit.id)
        self.assertEqual(updated_habit.action, 'Updated Action')

    def test_delete_habit(self):
        habit_data = {
            'user': self.user,
            'place': 'Test Place',
            'action': 'Test Action',
            'period': 7,
            'reward': 'Test Reward',
            'max_time_processing': 3600,
        }
        habit = Habit.objects.create(**habit_data)
        habit.delete()
        self.assertEqual(Habit.objects.count(), 0)
