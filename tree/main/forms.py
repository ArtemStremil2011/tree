from django import forms
from django.core.exceptions import ValidationError
from .models import Person, PersonFile

from django import forms
from .models import Person, PersonFile

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'info', 'parent', 'level', 'avatar']  # Добавил info
        widgets = {
            'info': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Биография, даты жизни, интересные факты...'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['parent'].queryset = Person.objects.filter(user=user)
    
    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        # Дополнительная проверка при создании/редактировании
        if parent and self.user and parent.user != self.user:
            raise ValidationError("Нельзя выбрать чужого человека как родителя!")
        return parent
    
    def clean(self):
        cleaned_data = super().clean()
        # Проверяем что уровень не отрицательный
        level = cleaned_data.get('level')
        if level is not None and level < 0:
            raise ValidationError({'level': 'Уровень не может быть отрицательным'})
        return cleaned_data

class PersonFileForm(forms.ModelForm):
    class Meta:
        model = PersonFile
        fields = ['person', 'file', 'description']  # Явно указываем поля, а не '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Описание файла (необязательно)'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем пользователя
        super().__init__(*args, **kwargs)
        
        # Ограничиваем выбор человека только своими
        if self.user:
            self.fields['person'].queryset = Person.objects.filter(user=self.user)
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Проверка размера файла (например, максимум 10MB)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError('Файл слишком большой. Максимальный размер 10MB')
            
            # Проверка расширения файла
            ext = file.name.split('.')[-1].lower()
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt', 'doc', 'docx']
            if ext not in allowed_extensions:
                raise ValidationError(f'Недопустимый формат файла. Разрешены: {", ".join(allowed_extensions)}')
        return file
    
    def clean_person(self):
        person = self.cleaned_data.get('person')
        if person and self.user and person.user != self.user:
            raise ValidationError("Нельзя прикрепить файл к чужому человеку!")
        return person