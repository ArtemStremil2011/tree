from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # ← теперь здесь home
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
    path('people/', views.person_list, name='person_list'),
    path('new_person/', views.new_person, name='new_person'),
    path('new_person_file/<int:person_id>/', views.new_person_file, name='new_person_file'),
    path('edit_person/<int:person_id>/', views.edit_person, name='edit_person'),
    path('delete_person/<int:person_id>/', views.delete_person, name='delete_person'),
]