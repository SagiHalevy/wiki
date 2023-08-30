from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("addpage", views.addpage, name="addpage"),
    path("wiki/<str:title>/editpage", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage"),
    
]
