from collections import UserDict
from importlib.metadata import requires
from re import T
from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from django.db.models.enums import Choices
from django.db.models.fields import CharField
from multiselectfield import MultiSelectField
from itertools import chain
from django.contrib.auth import get_user_model 


# Create your models here.

perguntas = [
    "id", "nome", "sobrenome",
    "Quais os motivos que te levaram a abrir um perfil profissional? ",
    "Como você vê o seu perfil em 5 anos? E em 10? ",
    "Seu perfil pode ser outra coisa no futuro ou atuar em outro segmento? Se sim, o que seria? ",
    "O que te fez me procurar para criar um projeto de Identidade Visual. Por que isso é importante pra você e para seu instagram? ",
    "Por que você acredita que as pessoas precisam da sua conta profissional? ",
    "Defina resumidamente do que se trata sua rede social: ",
    "Há quanto tempo sua rede social profissional existe? ",
    "O que faz sua rede social ser especial? ",
    "Sua rede social tem algum slogan? ",
    "Sua rede social tem concorrentes? Quem são? Fale um pouco sobre eles se achar necessário. Coloque nomes e links se puder: ",
    "Seus concorrentes oferecem algo que você não oferece? ",
    "Quais missões, visões e valores da sua conta social profissional? ",
    "Qual a Faixa Etária e Classe Social? ",
    "Gênero: ",
    "Quem são eles? Descreva com suas palavras. ",
    "Como você gostaria que os clientes descrevessem seu instagram?",
    "De que forma você espera que seu cliente encontre seu instagram?",
    "Quais os locais você acredita que seu cliente mais verá o logotipo do seu instagram. Acrescente por ordem de importância.",
    "Se seu instagram fosse uma pessoa como ela seria? Escolha quantas opções julgar necessário: ",
    "Dessas palavras que você escolheu, cite 3 que você considera mais forte. ",
    "Se seu instagram fosse uma pessoa, como ele seria? ",
    "Se necessário, adicione mais algumas características. ",
    "Há alguma cor que você queira na sua marca? ",
    "Há alguma cor que você NÃO queira na sua marca? ",
    "Há algum elemento que você NÃO queira na sua marca? ",
    "Pensando apenas em aspectos visuais, selecione alguns atributos que têm alguma relação com a sua marca. ",
    "Fique a vontade para dizer mais sobre a sua empresa ou dar considerações finais.",
    "Tem alguma referência?",
    "cliente"
]

"""

perguntas = {
    "id": "",
    "nome": "",
    "sobrenome": "",
    "Quais os motivos que te levaram a abrir um perfil profissional? ": "",
    "Como você vê o seu perfil em 5 anos? E em 10? ": "",
    "Seu perfil pode ser outra coisa no futuro ou atuar em outro segmento? Se sim, o que seria? ": "",
    "O que te fez me procurar para criar um projeto de Identidade Visual. Por que isso é importante pra você e para seu instagram? ": "",
    "Por que você acredita que as pessoas precisam da sua conta profissional? ": "",
    "Defina resumidamente do que se trata sua rede social: ": "",
    "Há quanto tempo sua rede social profissional existe? ": "",
    "O que faz sua rede social ser especial? ": "",
    "Sua rede social tem algum slogan? ": "",
    "Sua rede social tem concorrentes? Quem são? Fale um pouco sobre eles se achar necessário. Coloque nomes e links se puder: ": "",
    "Seus concorrentes oferecem algo que você não oferece? ": "",
    "Quais missões, visões e valores da sua conta social profissional? ": "",
    "Qual a Faixa Etária e Classe Social? ": "",
    "Gênero: ": "",
    "Quem são eles? Descreva com suas palavras. ": "",
    "Como você gostaria que os clientes descrevessem seu instagram?": "",
    "De que forma você espera que seu cliente encontre seu instagram?": "",
    "Quais os locais você acredita que seu cliente mais verá o logotipo do seu instagram. Acrescente por ordem de importância.": "",
    "Se seu instagram fosse uma pessoa como ela seria? Escolha quantas opções julgar necessário: ": "",
    "Dessas palavras que você escolheu, cite 3 que você considera mais forte. ": "",
    "Se seu instagram fosse uma pessoa, como ele seria? ": "",
    "Se necessário, adicione mais algumas características. ": "",
    "Há alguma cor que você queira na sua marca? ": "",
    "Há alguma cor que você NÃO queira na sua marca? ": "",
    "Há algum elemento que você NÃO queira na sua marca? ": "",
    "Pensando apenas em aspectos visuais, selecione alguns atributos que têm alguma relação com a sua marca. ": "",
    "Fique a vontade para dizer mais sobre a sua empresa ou dar considerações finais.": "",
    "Tem alguma referência?": ""
}
"""
def to_dict(Briefing):
    opts = Briefing._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(Briefing)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(Briefing)]

    return data

class Foto(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    nome = models.CharField(max_length=50, default=User)
    imagem = models.ImageField(null=False, blank=False)
    data = models.DateField(blank=True)
    legenda = models.TextField(max_length=2200)

    def __str__(self):
        return (f'Postagem {self.nome} | {self.data}')


class Video(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    nome = models.CharField(max_length=50, default=User)
    video = models.FileField(null=False, blank=False)
    data = models.DateField(blank=True)
    legenda = models.TextField(max_length=2200)

    def __str__(self):
        return (f'Postagem {self.nome} | {self.data}')


class Calendario(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    data = models.DateField()
    programacao = models.TextField(max_length=500)
    foto = models.ForeignKey(Foto, on_delete=models.PROTECT, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return (f'Programação de {self.data} | {self.cliente}')




GENERO_CHOICES = (
    ("Totalmente masculino", "Totalmente masculino"),
    ("Masculino predominante, pouco feminino", "Masculino predominante, pouco feminino"),
    ("Ambos os gêneros", "Ambos os gêneros"),
    ("Feminino predominante, pouco masculino", "Feminino predominante, pouco masculino"),
    ("Totalmente feminino", "Totalmente feminino")
)


PERSONALIDADE_CHOICES = (
    ("Séria", "Séria"), ("Alegre", "Alegre"), ("Conservadora", "Conservadora"), ("Nerd", "Nerd"),
    ("Discreta", "Discreta"), ("Sensível", "Sensível"), ("Aventureira", "Aventureira"), ("Tradicional", "Tradicional"),
    ("Líder", "Líder"), ("Sábia", "Sábia"), ("Exclusiva", "Exclusiva"), ("Científica", "Científica"),
    ("Técnica", "Técnica"), ("Grande", "Grande"), ("Complexa", "Complexa"), ("Rústica", "Rústica"),
    ("Futurista", "Futurista"),("Racional", "Racional"),("Mente Aberta", "Mente Aberta"),("Divertida", "Divertida"),
    ("Emocional", "Emocional"), ("Intuitiva", "Intuitiva"), ("Diferente", "Diferente"), ("Curiosa", "Curiosa"),
    ("Disciplinada", "Disciplinada"), ("Respeitadora", "Respeitadora"), ("Arrojada", "Arrojada"), ("Séria", "Séria"),
    ("Acessível", "Acessível"), ("Reservada", "Reservada"), ("Esperta", "Esperta"), ("Atual", "Atual"),
    ("Inocente", "Inocente"), ("Acadêmica", "Acadêmica"), ("Sutil", "Sutil"), ("Básica", "Básica"),
    ("Rigorosa", "Rigorosa"), ("Idealista", "Idealista"), ("Pequena", "Pequena"), ("Radical", "Radical"),
    ("Grosseira", "Grosseira"), ("Previsível", "Previsível"), ("Pessimista", "Pessimista"), ("Refinada", "Refinada"),
    ("Da Massa", "Da Massa"), ("Industrial", "Industrial"), ("Comum", "Comum"), ("Extrovertida", "Extrovertida"),
    ("Brincalhona", "Brincalhona"), ("Moderna", "Moderna"), ("Elegante", "Elegante"), ("Delicada", "Delicada"),
    ("Madura", "Madura"), ("Rebelde", "Rebelde"), ("Calma", "Calma"), ("Energética", "Energética"),
    ("Criativa", "Criativa"), ("Romântica", "Romântica"), ("Ousada", "Ousada"), ("Arrogante", "Arrogante"),
    ("Sóbria", "Sóbria"), ("Formal", "Formal"), ("Antiga", "Antiga"), ("Determinada", "Determinada"),
    ("Relaxada", "Relaxada"), ("Irreverente", "Irreverente"), ("Tranquila", "Tranquila"), ("Confiável", "Confiável"),
    ("Persistente", "Persistente"), ("Profissional", "Profissional"), ("Analítica", "Analítica"), ("Artística", "Artística"),
    ("Modesta", "Modesta"), ("Deslumbrante", "Deslumbrante"), ("Padronizada", "Padronizada"), ("Livre", "Livre"),
    ("Estável", "Estável"), ("Moderna", "Moderna"), ("Casual", "Casual"), ("Sonhadora", "Sonhadora"),
    ("Agressiva", "Agressiva"), ("Convencional", "Convencional"), ("Simples", "Simples"), ("Atrevida", "Atrevida"),
    ("Cotidiana", "Cotidiana"), ("Multifacetada", "Multifacetada"), ("Promissora", "Promissora"), ("Enigmática", "Enigmática"),
    ("Nostálgica", "Nostálgica"), ("Outro", "Outra")
)

ASPECTOS_CHOICES = (
    ("Séria", "Séria"), ("Conservadora", "Conservadora"), ("Aconchegante", "Aconchegante"), ("Moderna", "Moderna"),
    ("Sofisticada", "Sofisticada"), ("Vibrante", "Vibrante"), ("Retrô", "Retrô"), ("Pesada", "Pesada"),
    ("Rústica", "Rústica"), ("Extravagante", "Extravagante"), ("Popular", "Popular"), ("Formal", "Formal"),
    ("Humana", "Humana"), ("Irreverente", "Irreverente"), ("Extrovertida", "Extrovertida"), ("Alegre", "Alegre"),
    ("Delicada", "Delicada"), ("Orgânica", "Orgânica"), ("Elegante", "Elegante"), ("Tradicional", "Tradicional"),
    ("Digital", "Digital"), ("Leve", "Leve"), ("Discreta", "Discreta"), ("Nobre", "Nobre"),
    ("Romântica", "Romântica"), ("Ousada", "Ousada"), ("Rebelde", "Rebelde"), ("Outra", "Outra"),
)

User = get_user_model()
class Briefing(models.Model):
    # Fase 1
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=100)
    motivos = models.CharField(verbose_name="Quais os motivos que te levaram a abrir um perfil profissional?", max_length=2200)
    perfil = models.CharField(verbose_name="Como você vê o seu perfil em 5 anos? E em 10?", max_length=2200)
    segmento = models.CharField(verbose_name="Seu perfil pode ser outra coisa no futuro ou atuar em outro segmento? Se sim, o que seria?", max_length=2200)
    projeto_identidade = models.CharField(verbose_name="O que te fez me procurar para criar um projeto de Identidade Visual. Por que isso é importante pra você e para seu instagram?", max_length=2200)
    conta_profissional = models.CharField(verbose_name="Por que você acredita que as pessoas precisam da sua conta profissional?", max_length=2200)
    # Fase 2 
    rede_social = models.CharField(verbose_name="Defina resumidamente do que se trata sua rede social", max_length=2200)
    rede_profissional = models.CharField(verbose_name="Há quanto tempo sua rede social profissional existe?", max_length=2200)
    rede_especial = models.CharField(verbose_name="O que faz sua rede social ser especial?", max_length=2200)
    slogan = models.CharField(verbose_name="Sua rede social tem algum slogan?", max_length=2200)
    concorrentes = models.CharField(verbose_name="Sua rede social tem concorrentes? Quem são? Fale um pouco sobre eles se achar necessário. Coloque nomes e links se puder", max_length=2200)
    concorrentes_oferecem = models.CharField(verbose_name="Seus concorrentes oferecem algo que você não oferece?", max_length=2200)
    missoes = models.CharField(verbose_name="Quais missões, visões e valores da sua conta social profissional?", max_length=2200)
    # Fase 3
    faixa_etaria_social = models.CharField(verbose_name="Qual a Faixa Etária e Classe Social?", max_length=500)
    genero = models.CharField(verbose_name="Gênero", max_length=38, choices=GENERO_CHOICES)
    quem = models.CharField(verbose_name="Quem são eles? Descreva com suas palavras.", max_length=500)
    descricao_clientes = models.CharField(verbose_name="Como você gostaria que os clientes descrevessem seu instagram?", max_length=500)
    encontrar_clientes = models.CharField(verbose_name="De que forma você espera que seu cliente encontre seu instagram?", max_length=500)
    logotipo_clientes = models.CharField(verbose_name="Quais os locais você acredita que seu cliente mais verá o logotipo do seu instagram. Acrescente por ordem de importância.", max_length=500)
    # Fase 4
    personalidade = MultiSelectField(verbose_name="Se seu instagram fosse uma pessoa como ela seria? Escolha quantas opções julgar necessário:" ,max_length=1500, choices=PERSONALIDADE_CHOICES)
    palavras = models.CharField(verbose_name="Dessas palavras que você escolheu, cite 3 que você considera mais forte.", max_length=64)
    pessoa = models.CharField(verbose_name="Se seu instagram fosse uma pessoa, como ele seria?", max_length=500)
    caracteristicas = models.CharField(verbose_name="Se necessário, adicione mais algumas características.", max_length=100, null=True, blank=True)
    cor = models.CharField(verbose_name="Há alguma cor que você queira na sua marca?", max_length=100)
    nao_cor = models.CharField(verbose_name="Há alguma cor que você NÃO queira na sua marca?", max_length=100)
    nao_elemento = models.CharField(verbose_name="Há algum elemento que você NÃO queira na sua marca?", max_length=100)
    aspectos = MultiSelectField(verbose_name="Pensando apenas em aspectos visuais, selecione alguns atributos que têm alguma relação com a sua marca.", max_length=500, choices=ASPECTOS_CHOICES)
    consideracoes = models.CharField(verbose_name="Fique a vontade para dizer mais sobre a sua empresa ou dar considerações finais.", max_length=500)
    referencias = models.CharField(verbose_name="Tem alguma referência?", max_length=500, help_text="Referências de imagens ou de marcas que você gosta é muito válido, embora nós iremos montar nossa própria identidade visual.")
    cliente = models.ForeignKey(User, on_delete=models.PROTECT, default=User, null=True)
    # cliente = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return (f'{self.nome} {self.sobrenome} | Briefing - Identidade Visual')

    



def organizar(briefings):
    briefings = briefings
    listas = dict()
    unilist = dict()
    lista_final = dict()
    nome = ''
    provisorias = dict()
    listinha = dict()

    for a, b in enumerate(briefings):
        provisorias[a] = to_dict(b)

    for k, v in provisorias.items():
        for a, b in enumerate(v.values()):
            listinha[perguntas[a]] = b
        listas[k] = listinha.copy()
        listinha = {}

    for di in listas:
        for k, v in listas[di].items():
            if k == 'nome':
                nome += v
            elif k == 'sobrenome':
                nome += f' {v}'
            else:
                unilist[k] = v
            #print(k, v)
        lista_final[nome] = unilist
        unilist = {}
        nome=''

    return(lista_final)
    # print(listas)
    
    #for briefing in briefings:
    #    relatorios = to_dict(briefing)
    #    lista.append(relatorios)

    #for relatorio in lista:
    #    for question, answers in relatorio.items():
    #        print(question, answers)

    #return(relatorios)

