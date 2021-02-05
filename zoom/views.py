from django.shortcuts import render

def zoom(request):
    context = {}
    return render(request, 'zoom/index.html', context)