from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('sales:home')
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #Если запрос имеет продолжение адреса - после аутентификации отправить пользователя по этому запросу
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                #Если запрос не имеет продолжения, отправить в приложение sales по пути home
                else:
                    return redirect('sales:home')
        else:
            error_message = 'Что то пошло не так!'
    context = {
        'error_message': error_message,
        'form': form,
    }
    return render(request, 'auth/login.html' ,context=context)