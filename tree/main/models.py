from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='people', null=True, blank=True)
    name = models.CharField(max_length=100)
    info = models.CharField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    level = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

def person_file_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return f"person_files/{instance.person.name}/{new_filename}"

class PersonFile(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=person_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.person.name} - {self.description or self.file.name}" 