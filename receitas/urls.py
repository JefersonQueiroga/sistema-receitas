from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar-receitas/', views.buscar_receitas, name='buscar_receitas'),
    path('detalhe-receita/<int:id>/', views.detalhe_receita, name='detalhe_receita'),
]