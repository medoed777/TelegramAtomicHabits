from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from django_celery_beat.models import PeriodicTask
from habits.models import Habit
from habits.paginators import HabitsPagination
from habits.serializers import HabitsSerializer, PublicHabitsSerializer
from habits.services import set_schedule
from users.permissions import IsOwner


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitsSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        self._update_habit(habit)

    def _update_habit(self, habit):
        if not habit.is_pleasant:
            habit.save()

            if habit.user.tg_chat_id:
                set_schedule(habit)


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
            habit.save()

            if habit.user.tg_chat_id:
                try:
                    task = get_object_or_404(PeriodicTask, name=f"Habit Task - {habit.pk}")
                    task.enabled = False
                    task.delete()
                except PeriodicTask.DoesNotExist:
                    pass

                set_schedule(habit)


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
    serializer_class = HabitsSerializer
