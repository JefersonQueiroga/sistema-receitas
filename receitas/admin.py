from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')

@admin.register(models.Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'dificuldade', 'tempo_preparo')

@admin.register(models.Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nome',)

    