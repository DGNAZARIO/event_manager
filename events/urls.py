from django.urls import path
from .views import lista_eventos, detalhes_evento

urlpatterns = [
    path('', lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', detalhes_evento, name='detalhes_evento'),
]