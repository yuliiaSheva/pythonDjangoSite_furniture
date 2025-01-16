from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from traitlets import Instance

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm

# Create your views here.
def login(request):
    if request.method =='POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{ username }, You are enter")
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()


    context = {
        'title':'Home - Autorization',
        'form': form
    }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method =='POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f"{ user.username }, You are success registration and enter")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title':'Home - registration',
        'form': form
    }

    return render(request, 'users/registration.html', context)

@login_required
def profile(request) -> HttpResponseRedirect | HttpResponse:
    if request.method == 'POST':
        form = ProfileForm(data=request.POST,instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Frofile reloaded")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
    context = {
        'title':'Home - Profile',
        'form': form
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    messages.success(request, f"{ request.user.username }, You are exid")
    auth.logout(request)
    return redirect(reverse('main:index'))
