"""
URLs de la aplicacion planner.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('agenda/', views.agenda, name='agenda'),
    path('agenda/add/', views.agenda_add, name='agenda_add'),
    path('agenda/edit/<int:item_id>/', views.agenda_edit, name='agenda_edit'),
    path('agenda/delete/<int:item_id>/', views.agenda_delete, name='agenda_delete'),
    path('agenda/move/<int:item_id>/', views.agenda_move, name='agenda_move'),
    path('media/delete/<int:media_id>/', views.media_delete, name='media_delete'),
    path('media/reorder/', views.media_reorder, name='media_reorder'),
]
