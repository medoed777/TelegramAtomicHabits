from celery import shared_task
from habits.models import Habit
from dotenv import load_dotenv
import os
import telebot

load_dotenv()


@shared_task
def habits_notification(object_pk):
    habit = Habit.objects.get(pk=object_pk)
    bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
    message = (f'Трекер привычек напоминает: требуется совершить '
               f'{habit.action} в {habit.time} в {habit.place}')
    bot.send_message(habit.user.chat_id, message)
