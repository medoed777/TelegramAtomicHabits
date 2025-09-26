from django.shortcuts import get_object_or_404, render
from rest_framework import generics

from habits.models import Habit
from habits.paginators import HabitsPagination
from habits.serializers import HabitsSerializer, PublicHabitsSerializer
# from habits.services import create_replacements, create_schedule, create_task, make_replacements
from users.permissions import IsOwner


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitsSerializer

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        if not habit.is_pleasant:
            replacements = create_replacements(habit)
            habit.frequency = make_replacements(habit.frequency, replacements)
            habit.save()

            if habit.user.tg_chat_id:
                schedule = create_schedule(habit.frequency)
                create_task(schedule, habit)


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = PublicHabitsSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitsSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = (IsOwner,)


class HabitUpdateAPIView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = (IsOwner,)

    def perform_update(self, serializer):
        habit = serializer.save(user=self.request.user)
        if not habit.is_pleasant:
            replacements = create_replacements(habit)
            habit.frequency = make_replacements(habit.frequency, replacements)
            habit.save()

            if habit.user.tg_chat_id:
                task = get_object_or_404(PeriodicTask, name=f"Sending reminder {habit.pk}")
                schedule = create_schedule(habit.frequency)
                if task:
                    task.enabled = False
                    task.delete()
                create_task(schedule, habit)


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
    serializer_class = HabitsSerializer
