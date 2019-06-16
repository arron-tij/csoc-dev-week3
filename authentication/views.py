from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from authentication.forms import SignUpForm
# Create your views here.


def loginView(request):
    pass

def logoutView(request):
    pass



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)    
            login(request,user)
            return redirect('/books/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})