from django.shortcuts import render

def stats_home(request):
    return render(request, 'stats_home.html', {})
