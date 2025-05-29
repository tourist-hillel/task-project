from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from tasks_api.models import Task
from tasks_api.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)
        completed = self.request.query_params.get('completed', None)
        priority = self.request.query_params.get('priority', None)

        if completed:
            qs = qs.filter(completed=completed.lower() == 'true')
        if priority:
            qs = qs.filter(priority=priority)

        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'This username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)

