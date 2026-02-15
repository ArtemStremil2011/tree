from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Person
from .forms import PersonForm, PersonFileForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'main/home.html')

@login_required
def person_list(request):
    # Только СВОИ люди
    people = Person.objects.filter(user=request.user).order_by('level')
    return render(request, 'main/person_list.html', {'people': people})

@login_required
def person_detail(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    # Проверяем, что человек принадлежит текущему пользователю
    if person.user != request.user:
        raise Http404("Это не ваш предок!")
    return render(request, 'main/person_detail.html', {'person': person})

@login_required
def new_person(request):
    if request.method != 'POST':
        form = PersonForm(user=request.user)  # ← передаем пользователя
    else:
        form = PersonForm(request.POST, request.FILES, user=request.user)  # ← и здесь
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            return redirect('person_list')
    return render(request, 'main/new_person.html', {'form': form})

@login_required
def edit_person(request, person_id):
    person = get_object_or_404(Person, id=person_id, user=request.user)
    
    if request.method != 'POST':
        form = PersonForm(instance=person, user=request.user)  # ← передаем пользователя
    else:
        form = PersonForm(request.POST, request.FILES, instance=person, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('person_detail', person_id=person.id)
    return render(request, 'main/edit_person.html', {'form': form, 'person': person})

@login_required
def new_person_file(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    # Проверяем, что человек принадлежит текущему пользователю
    if person.user != request.user:
        raise Http404("Это не ваш предок!")
    
    if request.method != 'POST':
        form = PersonFileForm(initial={'person': person})
    else:
        form = PersonFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save(commit=False)
            file_obj.person = person
            file_obj.save()
            return redirect('person_detail', person_id=person_id)
    return render(request, 'main/new_person_file.html', {'form': form, 'person': person})



@login_required
def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    # Проверяем, что человек принадлежит текущему пользователю
    if person.user != request.user:
        raise Http404("Это не ваш предок!")
    
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    
    return render(request, 'main/delete_person.html', {'person': person})