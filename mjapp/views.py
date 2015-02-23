from django.shortcuts import redirect

def home(request):
    return redirect('/stats/lmc-season-2')
