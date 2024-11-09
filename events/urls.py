from .views import lista_eventos, detalhes_evento
from django.urls import path
from . import views

urlpatterns = [
    path('', lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', detalhes_evento, name='detalhes_evento'),
    path('', views.event_list, name='lista_eventos'),
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('<int:event_id>/', views.event_detail, name='detalhes_evento'),
    path('registration/<int:registration_id>/edit/', views.edit_registration, name='edit_registration'),
    path('registration/<int:registration_id>/delete/', views.delete_registration, name='delete_registration'),
]