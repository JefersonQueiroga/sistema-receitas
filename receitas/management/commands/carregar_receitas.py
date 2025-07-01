# management/commands/carregar_receitas.py
# Coloque este arquivo em: myapp/management/commands/carregar_receitas.py

import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings
from receitas.models import Categoria, Receita, Ingrediente, ReceitaIngrediente


class Command(BaseCommand):
    help = 'Carrega dados iniciais para o aplicativo de receitas'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpa todos os dados existentes antes de carregar novos dados',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Exibe informações detalhadas durante a execução',
        )
    
    def handle(self, *args, **options):
        self.verbose = options['verbose']
        
        try:
            with transaction.atomic():
                if options['clear']:
                    self.limpar_dados()
                
                self.criar_categorias()
                self.criar_ingredientes()
                self.criar_receitas()
                
                self.exibir_estatisticas()
                
        except Exception as e:
            raise CommandError(f'Erro ao carregar dados: {str(e)}')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Dados carregados com sucesso!')
        )
    
    def limpar_dados(self):
        """Remove todos os dados existentes"""
        self.stdout.write("🗑️  Limpando dados existentes...")
        
        ReceitaIngrediente.objects.all().delete()
        Receita.objects.all().delete()
        Ingrediente.objects.all().delete()
        Categoria.objects.all().delete()
        
        if self.verbose:
            self.stdout.write("   Todos os dados foram removidos")
    
    def criar_categorias(self):
        """Cria as categorias de receitas"""
        self.stdout.write("📂 Criando categorias...")
        
        categorias_data = [
            {"nome": "Massas", "descricao": "Pratos com massas como macarrão, lasanha, nhoque"},
            {"nome": "Carnes", "descricao": "Pratos principais com carne bovina, suína, frango"},
            {"nome": "Sobremesas", "descricao": "Doces, bolos, tortas e outras sobremesas"},
            {"nome": "Saladas", "descricao": "Saladas frescas e nutritivas"},
            {"nome": "Sopas", "descricao": "Sopas e caldos reconfortantes"},
            {"nome": "Peixes", "descricao": "Pratos com peixes e frutos do mar"},
            {"nome": "Vegetariano", "descricao": "Pratos sem carne"},
            {"nome": "Lanches", "descricao": "Sanduíches, salgados e petiscos"},
        ]
        
        self.categorias = {}
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data["nome"],
                defaults=cat_data
            )
            self.categorias[cat_data["nome"]] = categoria
            
            if self.verbose:
                status = "criada" if created else "já existe"
                self.stdout.write(f"   📁 {categoria.nome} ({status})")
        
        self.stdout.write(f"   ✅ {len(self.categorias)} categorias processadas")
    
    def criar_ingredientes(self):
        """Cria os ingredientes"""
        self.stdout.write("🥕 Criando ingredientes...")
        
        ingredientes_lista = [
            "Macarrão", "Molho de tomate", "Queijo parmesão", "Alho", "Cebola",
            "Azeite", "Sal", "Pimenta do reino", "Manjericão", "Orégano",
            "Frango", "Carne moída", "Bacon", "Ovos", "Leite",
            "Farinha de trigo", "Açúcar", "Manteiga", "Chocolate", "Baunilha",
            "Tomate", "Alface", "Cenoura", "Batata", "Cebola roxa",
            "Abobrinha", "Brócolis", "Couve-flor", "Pimentão", "Pepino",
            "Salmão", "Camarão", "Atum", "Limão", "Salsa",
            "Arroz", "Feijão", "Quinoa", "Grão de bico", "Lentilha",
            "Pão", "Presunto", "Queijo mussarela", "Tomate cereja", "Rúcula",
            "Creme de leite", "Champignon", "Vinho branco", "Caldo de galinha", "Noz moscada"
        ]
        
        self.ingredientes = {}
        created_count = 0
        
        for nome in ingredientes_lista:
            ingrediente, created = Ingrediente.objects.get_or_create(nome=nome)
            self.ingredientes[nome] = ingrediente
            
            if created:
                created_count += 1
            
            if self.verbose:
                status = "criado" if created else "já existe"
                self.stdout.write(f"   🥬 {ingrediente.nome} ({status})")
        
        self.stdout.write(f"   ✅ {len(self.ingredientes)} ingredientes processados ({created_count} novos)")
    
    def criar_receitas(self):
        """Cria as receitas com seus ingredientes"""
        self.stdout.write("👨‍🍳 Criando receitas...")
        
        receitas_data = [
            {
                "titulo": "Espaguete à Carbonara",
                "descricao": "Massa italiana clássica com bacon, ovos e queijo",
                "modo_preparo": "1. Cozinhe o espaguete em água fervente com sal até ficar al dente.\n2. Em uma frigideira, frite o bacon até ficar crocante.\n3. Bata os ovos com queijo parmesão ralado.\n4. Escorra a massa e misture rapidamente com o bacon e a mistura de ovos.\n5. Tempere com pimenta do reino e sirva imediatamente.",
                "tempo_preparo": 20,
                "dificuldade": "M",
                "categoria": "Massas",
                "ingredientes": [
                    ("Macarrão", "400g"),
                    ("Bacon", "150g"),
                    ("Ovos", "3 unidades"),
                    ("Queijo parmesão", "100g"),
                    ("Pimenta do reino", "a gosto"),
                    ("Sal", "a gosto")
                ]
            },
            {
                "titulo": "Frango Grelhado com Salada",
                "descricao": "Peito de frango temperado com salada fresca",
                "modo_preparo": "1. Tempere o frango com alho, sal, pimenta e azeite.\n2. Deixe marinar por 30 minutos.\n3. Grelhe o frango por 6-8 minutos de cada lado.\n4. Prepare a salada com alface, tomate e cenoura.\n5. Sirva o frango com a salada e regue com azeite.",
                "tempo_preparo": 45,
                "dificuldade": "F",
                "categoria": "Carnes",
                "ingredientes": [
                    ("Frango", "4 filés"),
                    ("Alface", "1 pé"),
                    ("Tomate", "2 unidades"),
                    ("Cenoura", "1 unidade"),
                    ("Alho", "3 dentes"),
                    ("Azeite", "3 colheres de sopa"),
                    ("Sal", "a gosto"),
                    ("Pimenta do reino", "a gosto")
                ]
            },
            {
                "titulo": "Bolo de Chocolate",
                "descricao": "Bolo fofinho de chocolate para sobremesa",
                "modo_preparo": "1. Pré-aqueça o forno a 180°C.\n2. Misture os ingredientes secos em uma tigela.\n3. Em outra tigela, bata os ovos com açúcar até clarear.\n4. Adicione leite, manteiga e baunilha.\n5. Incorpore os ingredientes secos gradualmente.\n6. Asse por 35-40 minutos.",
                "tempo_preparo": 60,
                "dificuldade": "M",
                "categoria": "Sobremesas",
                "ingredientes": [
                    ("Farinha de trigo", "2 xícaras"),
                    ("Açúcar", "1,5 xícara"),
                    ("Chocolate", "200g"),
                    ("Ovos", "3 unidades"),
                    ("Leite", "1 xícara"),
                    ("Manteiga", "100g"),
                    ("Baunilha", "1 colher de chá")
                ]
            },
            {
                "titulo": "Salada Caesar",
                "descricao": "Salada clássica com alface, croutons e molho especial",
                "modo_preparo": "1. Lave e pique a alface romana.\n2. Prepare croutons tostando cubos de pão com alho e azeite.\n3. Misture azeite, limão, alho e parmesão para o molho.\n4. Monte a salada com alface, croutons e queijo.\n5. Regue com o molho na hora de servir.",
                "tempo_preparo": 25,
                "dificuldade": "F",
                "categoria": "Saladas",
                "ingredientes": [
                    ("Alface", "1 pé"),
                    ("Pão", "4 fatias"),
                    ("Queijo parmesão", "80g"),
                    ("Alho", "2 dentes"),
                    ("Limão", "1 unidade"),
                    ("Azeite", "4 colheres de sopa"),
                    ("Sal", "a gosto")
                ]
            },
            {
                "titulo": "Sopa de Legumes",
                "descricao": "Sopa nutritiva com diversos legumes",
                "modo_preparo": "1. Refogue cebola e alho no azeite.\n2. Adicione os legumes picados e refogue por mais 5 minutos.\n3. Cubra com caldo de galinha e deixe ferver.\n4. Cozinhe por 20 minutos até os legumes ficarem macios.\n5. Tempere com sal, pimenta e salsa.",
                "tempo_preparo": 40,
                "dificuldade": "F",
                "categoria": "Sopas",
                "ingredientes": [
                    ("Cenoura", "2 unidades"),
                    ("Batata", "2 unidades"),
                    ("Abobrinha", "1 unidade"),
                    ("Cebola", "1 unidade"),
                    ("Alho", "3 dentes"),
                    ("Caldo de galinha", "1 litro"),
                    ("Azeite", "2 colheres de sopa"),
                    ("Salsa", "a gosto")
                ]
            },
            {
                "titulo": "Salmão Grelhado",
                "descricao": "Filé de salmão grelhado com temperos especiais",
                "modo_preparo": "1. Tempere o salmão com sal, pimenta e limão.\n2. Deixe marinar por 15 minutos.\n3. Aqueça uma frigideira antiaderente.\n4. Grelhe o salmão por 4-5 minutos de cada lado.\n5. Finalize com salsa picada e sirva com legumes.",
                "tempo_preparo": 30,
                "dificuldade": "M",
                "categoria": "Peixes",
                "ingredientes": [
                    ("Salmão", "4 filés"),
                    ("Limão", "2 unidades"),
                    ("Salsa", "1 maço"),
                    ("Sal", "a gosto"),
                    ("Pimenta do reino", "a gosto"),
                    ("Azeite", "2 colheres de sopa")
                ]
            },
            {
                "titulo": "Risotto de Cogumelos",
                "descricao": "Risotto cremoso com champignons",
                "modo_preparo": "1. Refogue cebola no azeite até dourar.\n2. Adicione arroz e refogue por 2 minutos.\n3. Adicione vinho branco e deixe evaporar.\n4. Vá adicionando caldo quente aos poucos, mexendo sempre.\n5. Incorpore champignons e queijo parmesão no final.",
                "tempo_preparo": 45,
                "dificuldade": "D",
                "categoria": "Vegetariano",
                "ingredientes": [
                    ("Arroz", "300g"),
                    ("Champignon", "200g"),
                    ("Cebola", "1 unidade"),
                    ("Vinho branco", "100ml"),
                    ("Caldo de galinha", "1 litro"),
                    ("Queijo parmesão", "100g"),
                    ("Azeite", "3 colheres de sopa")
                ]
            },
            {
                "titulo": "Sanduíche Natural",
                "descricao": "Sanduíche saudável com peito de peru e salada",
                "modo_preparo": "1. Corte o pão pela metade.\n2. Passe uma camada fina de manteiga.\n3. Monte com alface, tomate, cenoura ralada e presunto.\n4. Adicione queijo e tempere com sal e orégano.\n5. Feche o sanduíche e sirva.",
                "tempo_preparo": 10,
                "dificuldade": "F",
                "categoria": "Lanches",
                "ingredientes": [
                    ("Pão", "4 fatias"),
                    ("Presunto", "8 fatias"),
                    ("Queijo mussarela", "4 fatias"),
                    ("Alface", "4 folhas"),
                    ("Tomate", "1 unidade"),
                    ("Cenoura", "1/2 unidade"),
                    ("Manteiga", "2 colheres de sopa")
                ]
            }
        ]
        
        created_count = 0
        
        for receita_data in receitas_data:
            ingredientes_receita = receita_data.pop("ingredientes")
            categoria_nome = receita_data.pop("categoria")
            
            receita, created = Receita.objects.get_or_create(
                titulo=receita_data["titulo"],
                defaults={
                    **receita_data,
                    "categoria": self.categorias[categoria_nome]
                }
            )
            
            if created:
                created_count += 1
                
                # Criando as relações receita-ingrediente
                for nome_ingrediente, quantidade in ingredientes_receita:
                    ReceitaIngrediente.objects.create(
                        receita=receita,
                        ingrediente=self.ingredientes[nome_ingrediente],
                        quantidade=quantidade
                    )
            
            if self.verbose:
                status = "criada" if created else "já existe"
                self.stdout.write(f"   🍽️  {receita.titulo} ({status})")
        
        self.stdout.write(f"   ✅ {Receita.objects.count()} receitas processadas ({created_count} novas)")
    
    def exibir_estatisticas(self):
        """Exibe estatísticas dos dados carregados"""
        self.stdout.write("\n" + "="*50)
        self.stdout.write("📊 ESTATÍSTICAS FINAIS")
        self.stdout.write("="*50)
        
        self.stdout.write(f"📂 Categorias: {Categoria.objects.count()}")
        self.stdout.write(f"🥕 Ingredientes: {Ingrediente.objects.count()}")
        self.stdout.write(f"🍽️  Receitas: {Receita.objects.count()}")
        self.stdout.write(f"🔗 Relações receita-ingrediente: {ReceitaIngrediente.objects.count()}")
        
        self.stdout.write("\n📂 Receitas por categoria:")
        for categoria in Categoria.objects.all():
            count = categoria.receita_set.count()
            self.stdout.write(f"   • {categoria.nome}: {count} receita(s)")
        
        self.stdout.write("\n⭐ Receitas por dificuldade:")
        for choice in Receita.DIFICULDADE_CHOICES:
            count = Receita.objects.filter(dificuldade=choice[0]).count()
            self.stdout.write(f"   • {choice[1]}: {count} receita(s)")
        
        # Tempo médio de preparo
        from django.db.models import Avg
        tempo_medio = Receita.objects.aggregate(Avg('tempo_preparo'))['tempo_preparo__avg']
        if tempo_medio:
            self.stdout.write(f"\n⏱️  Tempo médio de preparo: {tempo_medio:.1f} minutos")