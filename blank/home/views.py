from django.shortcuts import render

# Create your views here.

def home(request):
    context = {
        'title': 'Онлайн сервис юридических документов'
    }
    return render(request, 'home/home.html', context)

