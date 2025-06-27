from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'receitas/index.html')


def buscar_receitas(request):
    return render(request, 'receitas/buscar_receitas.html')


def detalhe_receita(request, id):
    return render(request, 'receitas/detalhe_receita.html', {'id': id})
