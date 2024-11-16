from .views import lista_eventos, detalhes_evento
from django.urls import path
from . import views

urlpatterns = [
    path('', lista_eventos, name='lista_eventos'),
    path('events/events/evento/<int:id>/', views.detalhes_evento, name='detalhes_evento'),
    path('events/', views.lista_eventos, name='lista_eventos'),
    path('create/', views.create_event, name='create_event'),
    path('events/<int:evento_id>/edit/', views.edit_event, name='edit_event'),
    path('evento/<int:evento_id>/', views.detalhes_evento, name='detalhes_evento'),
    path('registration/<int:registration_id>/edit/', views.edit_registration, name='edit_registration'),
    path('registration/<int:registration_id>/delete/', views.delete_registration, name='delete_registration'),
    path('evento/<int:id>/delete/', views.deletar_evento, name='deletar_evento'),
]