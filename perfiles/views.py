from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms.register_form import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


def login_view(request):
    error_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error_message = "Credenciales invalidas."

    return render(request, "login.html", {"error": error_message})

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    else:
        print("dfffffffffff")
        return redirect("home")