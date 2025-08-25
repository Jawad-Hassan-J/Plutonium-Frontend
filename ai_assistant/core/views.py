# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html?utm_source

from django.shortcuts import render
from .router import execute

def home(request):
    result = None
    user_input_request = request.POST.get("user_input_request", "")
    user_input_file = request.FILES.get("user_input_file")

    if request.method == "POST":
        result = execute(user_input_request, user_input_file)

    return render(request, "home.html", {
        "user_input_request": user_input_request,
        "user_input_file": user_input_file,
        "result": result
    })
