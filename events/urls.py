from django.urls import path
from .views import (
    lista_eventos,
    detalhes_evento,
    create_event,
    edit_event,
    deletar_evento,
    listar_inscricoes,
    relatorio_inscricoes,
    exportar_inscricoes_csv,
    edit_registration,
    delete_registration,
)

urlpatterns = [
    # Eventos
    path('', lista_eventos, name='lista_eventos'),
    path('evento/<int:id>/', detalhes_evento, name='detalhes_evento'),
    path('evento/<int:id>/delete/', deletar_evento, name='deletar_evento'),
    path('evento/<int:evento_id>/edit/', edit_event, name='edit_event'),

    # Criação
    path('create/', create_event, name='create_event'),

    # Inscrições
    path('inscricoes/', listar_inscricoes, name='listar_inscricoes'),
    path('relatorio/inscricoes/', relatorio_inscricoes, name='relatorio_inscricoes'),
    path('evento/<int:evento_id>/exportar_inscricoes/', exportar_inscricoes_csv, name='exportar_inscricoes_csv'),

    # Registro de inscrições
    path('registration/<int:registration_id>/edit/', edit_registration, name='edit_registration'),
    path('registration/<int:registration_id>/delete/', delete_registration, name='delete_registration'),
]
