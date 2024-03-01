from django.urls import include, path

from . import views

urlpatterns = [
    path('categories', views.categories, name='categories'),
]
