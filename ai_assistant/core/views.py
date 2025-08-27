# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html?utm_source

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  
from .router import execute

def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def plutonium(request):
    result = None
    user_input_request = request.POST.get("user_input_request", "")
    user_input_file = request.FILES.get("user_input_file")

    if request.method == "POST":
        result = execute(user_input_request, user_input_file)

    return render(request, "plutonium.html", {
        "user_input_request": user_input_request,
        "user_input_file": user_input_file,
        "result": result
    })






