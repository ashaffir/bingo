from django.shortcuts import render


def frontend_index(request):
    return render(request, 'frontend/index.html')
