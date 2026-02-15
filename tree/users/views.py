from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method != 'POST':
        # GET запрос - показываем пустую форму
        form = UserCreationForm()
    else:
        # POST запрос - обрабатываем данные
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)  # автоматически входим после регистрации
            return redirect('person_list')  # редирект на страницу древа
    
    # Если форма невалидна или GET запрос
    context = {'form': form}
    return render(request, 'registration/register.html', context)   