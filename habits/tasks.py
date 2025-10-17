import requests
from celery import shared_task

from config.settings import TELEGRAM_BOT_TOKEN
from habits.models import Habit


@shared_task
def send_message(pk) -> None:
    """Функция напоминания пользователю."""
    habit = Habit.objects.get(pk=pk)
    text = (
        f"Трекер привычек напоминает: требуется совершить "
        f"{habit.action} в {habit.time} в {habit.place}"
        f"Не забудьте {habit.reward if habit.reward else habit.related_habit}."
    )
    params = {
        "text": text,
        "chat_id": habit.user.tg_chat_id,
    }
    requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params
    )
