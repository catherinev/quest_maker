from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'quest_maker_app/homepage.html', {})
