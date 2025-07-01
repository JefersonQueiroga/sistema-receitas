from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Receita(models.Model):
    DIFICULDADE_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Médio'), 
        ('D', 'Difícil')
    ]
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    modo_preparo = models.TextField()
    tempo_preparo = models.IntegerField()  # em minutos
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ingredientes = models.ManyToManyField('Ingrediente', through='ReceitaIngrediente')
    
class Ingrediente(models.Model):
    nome = models.CharField(max_length=50)
    
class ReceitaIngrediente(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.CharField(max_length=50)
