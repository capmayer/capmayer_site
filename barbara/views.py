from django.shortcuts import render

# Create your views here.
def view_init(request):
    return render(request, 'barbara/init.html', {})
