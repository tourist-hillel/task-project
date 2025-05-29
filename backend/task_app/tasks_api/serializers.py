from rest_framework import serializers
from tasks_api.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'completed', 'priority', 'created_at']
        read_only_fields = ['user']
