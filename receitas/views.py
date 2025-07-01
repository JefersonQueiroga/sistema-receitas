from django.shortcuts import render
from .models import Receita

# Create your views here.
def home(request):
    return render(request, 'receitas/index.html')


def buscar_receitas(request):
    receitas = Receita.objects.all()
    context = {
        'receitas': receitas
    }
    return render(request, 'receitas/buscar_receitas.html',context)


def detalhe_receita(request, id):
    return render(request, 'receitas/detalhe_receita.html', {'id': id})

