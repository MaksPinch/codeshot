from django.urls import reverse
from django.shortcuts import render
def home_view(request):
    data = {
        'title': 'Домашняя страница проекта CodeShot',
        'name': 'Максим'
    }
    return render(request, 'codeshot/home.html', context=data)

