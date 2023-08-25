from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to your desired page after login
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'accounts/custom_login.html')

def custom_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not username and not password1 and not password2:
            messages.error(request, 'All the fields are required, please fill them')
        
        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            messages.success(request, 'Account created and logged in successfully!')
            return redirect('home')  # Redirect to your desired page after signup
        else:
            messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'accounts/custom_signup.html')
