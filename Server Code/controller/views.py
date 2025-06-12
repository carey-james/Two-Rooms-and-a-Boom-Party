from django.shortcuts import render

def controller_screen(request):
    return render(request, 'controller/index.html', {})
