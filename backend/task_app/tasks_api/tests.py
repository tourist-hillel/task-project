import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from tasks_api.models import Task
from tasks_api.serializers import TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpwd')

@pytest.fixture
def token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@pytest.fixture
def authenticated_client(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.mark.django_db
def test_task_viewset_list(authenticated_client, user):
    Task.objects.create(user=user, title='Completed', completed=True, priority='low')
    response = authenticated_client.get('http://localhost:8000/api/tasks/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Completed'

@pytest.mark.django_db
def test_task_viewset_filter_completed(authenticated_client, user):
    Task.objects.create(user=user, title='Completed task', completed=True, priority='high')
    Task.objects.create(user=user, title='Incompleted task', completed=False, priority='high')
    response = authenticated_client.get('http://localhost:8000/api/tasks/?completed=true')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Completed task'

@pytest.mark.django_db
def test_task_viewset_filter_priority(authenticated_client, user):
    Task.objects.create(user=user, title='Low priority task', completed=True, priority='low')
    Task.objects.create(user=user, title='High priority task', completed=False, priority='high')
    response = authenticated_client.get('http://localhost:8000/api/tasks/?priority=high')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'High priority task'

@pytest.mark.django_db
def test_task_viewset_create_task(authenticated_client, user):
    data = {
        'title': 'New task',
        'description': 'Task description',
        'priority': 'medium'
    }
    response = authenticated_client.post('http://localhost:8000/api/tasks/', data, format='json')
    assert response.status_code == 201
    assert Task.objects.filter(user=user, title='New task').exists()