from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, UserUpdateForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "blog/login.html"


class CustomLogoutView(LogoutView):
    template_name = "blog/logout.html"


@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "blog/profile.html", {"form": form})

