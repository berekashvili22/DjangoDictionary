from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.views.generic import UpdateView
from . models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created, Log in now .')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def settings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('settings')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }
    return render(request, 'users/settings.html', context)

def update_profile(request):
    if request.method == 'POST':
        user = request.user
        imgName = request.POST['choice']
        image=f'{imgName}.png'
        Profile.objects.filter(user=user).update(image=image)

    return redirect('home')