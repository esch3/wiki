from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("save", views.save, name="save"),
    path("update", views.update, name="update"),
    path("search", views.search, name="search"),
    path("<str:title>", views.display, name="display") 
]
