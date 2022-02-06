from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from .models import Foto, Video, Calendario, Briefing, organizar, to_dict, perguntas, FotosPost
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from allauth.account.views import PasswordChangeView
from .forms import BriefingForm

""" 
Imports utilizados para gerar .pdf

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.lib.pagesizes import A4
from itertools import chain

"""




app_name = "medicos"

# Create your views here.

# View da Página Inicial
def PaginaInicial(request):
    return render(request, 'index.html')


# View do Painel principal
class Painel(LoginRequiredMixin, ListView):
    model = Briefing
    template_name = "painel.html"

    # Verificar se o cliente já fez o briefing ou não.
    def get_queryset(self):

        self.object_list = Briefing.objects.filter(cliente=self.request.user)
        print(self.request.user)
        print(Briefing.objects.filter(cliente=self.request.user))
        # Se o object_list não retorna nada, o cliente responde um formulário, se retornar o briefing, o cliente vai editar
        return self.object_list


# Página dos Posts (Fotos/Videos)
@login_required
def Posts(request):
    return render(request, "posts/postagens.html")


# Página das Fotos (Todas)
class FotosView(LoginRequiredMixin, ListView):
    model = Foto
    template_name = "posts/fotos.html"

    # Retorna apenas as fotos do cliente --> (filter(cliente=self.request.user))
    def get_queryset(self):

        self.object_list = Foto.objects.filter(cliente=self.request.user)
        return self.object_list


# Página da foto detalhada
@login_required
def viewFoto(request, pk):
    # Foto --> Thumbnail
    foto = Foto.objects.get(id=pk)
    # FotosPost --> Fotos para postar, baseada na foto principal (foto=foto)
    fotos = FotosPost.objects.filter(foto=foto)
    # Filtragem para apenas fotos dos usuarios
    all = (Foto.objects.filter(cliente=request.user))
    print((foto), list(fotos))
    # Listagem do all (Formato de Queryset -> Lista[])
    filtro = list(all)
    # Se o post tiver mais de uma foto, roda o template de carrosel
    if foto in filtro and list(fotos) != []:
        return render(request, 'posts/foto_carrosel.html', {'foto': foto, 'fotos': fotos})
    # Se o post tiver apenas uma foto, roda o template normal
    elif foto in filtro:
        return render(request, 'posts/foto.html', {'foto': foto})
    # Se a url retornar a foto de outra pessoa, roda o template indisponível
    else:
        return render(request, 'posts/indisponivel.html')


# Página dos vídeos
class VideosView(LoginRequiredMixin, ListView):
    model = Video
    template_name = "posts/videos.html"

    # Retorna apenas os vídeos do cliente --> (filter(cliente=self.request.user))
    def get_queryset(self):

        self.object_list = Video.objects.filter(cliente=self.request.user)
        return self.object_list


# Página detalhada do vídeo
@login_required
def viewVideo(request, pk):
    # Pega o vídeo pelo id
    video = Video.objects.get(id=pk)
    # Pega os videos do cliente
    all = (Video.objects.filter(cliente=request.user))
    # Usa o all (Todos os vídeos) como filtro do video, para que apenas o cliente possa acessar
    filtro = list(all)
    print(filtro)
    # Se for o próprio cliente
    if video in filtro:
        return render(request, 'posts/video.html', {'video': video})
    # Se for outro cliente o erro será tratado
    else:
        return render(request, 'posts/indisponivel.html')


# Página da programação dos clientes
class CalendarioView(LoginRequiredMixin, ListView):
    model = Calendario
    template_name = "calendario/calendario.html"

    # Retorna a lista de programações do cliente
    def get_queryset(self):

        self.object_list = Calendario.objects.filter(cliente=self.request.user)
        return self.object_list


# Página para editar perfil
class EditarPerfilView(UpdateView, LoginRequiredMixin):
    model = User
    template_name = 'account/perfil.html'
    # Campos para editar perfil
    fields = ["first_name", "last_name", "email"]
    success_url = reverse_lazy('painel')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(User, username=self.request.user)
        return self.object


# Página para editar senha
class EditarSenhaView(PasswordChangeView, LoginRequiredMixin):
    form_class = PasswordChangeForm
    template_name = 'account/senha.html'
    success_url = reverse_lazy('painel')


# Página para os formulários
# Não utilizado atualmente, pois só tem um formulário
class FormulariosView(LoginRequiredMixin, ListView):
    model = Briefing
    template_name = "formularios/formularios.html"

    def get_queryset(self):

        self.object_list = Briefing.objects.filter(cliente=self.request.user)
        print(self.request.user)
        print(Briefing.objects.filter(cliente=self.request.user))
        return self.object_list

#@login_required
#def FormulariosView(request):
#    return render(request, 'formularios/formularios.html')

"""
class BriefingView(LoginRequiredMixin, CreateView):
    model = Briefing
    fields = [
        'nome', 'sobrenome', 'motivos', 'perfil', 'segmento', 'projeto_identidade', 'conta_profissional',
        'rede_social', 'rede_profissional', 'rede_especial', 'slogan', 'concorrentes', 'concorrentes_oferecem', 'missoes',
        'faixa_etaria_social', 'genero', 'quem', 'descricao_clientes', 'encontrar_clientes', 'logotipo_clientes',
        'personalidade', 'palavras', 'pessoa', 'caracteristicas', 'cor', 'nao_cor', 'nao_elemento', 'aspectos', 'consideracoes', 'referencias'
        ]
    template_name = 'formularios/briefing.html'
    success_url = reverse_lazy('painel')
"""   

# View para o registro do formulário de identidade visual
@login_required
def BriefingView(request):
    # Método POST (Envio do formulário)
    if request.method == 'POST':
        form = BriefingForm(data=request.POST)
        if form.is_valid():
            form.save()
            briefing = form.save(commit=False) 
            briefing.cliente = request.user # the user must be logged in for this.
            briefing.save()
        return redirect('painel')
    # Método GET (O usuário vê o formulário)
    else:
        form = BriefingForm()

    return render(request, 'formularios/briefing.html', {"form": form})


# View para editar o formulário de identidade visual
class BriefingUpdateView(LoginRequiredMixin, UpdateView):
    model = Briefing
    template_name = 'formularios/briefing.html'
    fields = [
        'nome', 'sobrenome', 'motivos', 'perfil', 'segmento', 'projeto_identidade', 'conta_profissional',
        'rede_social', 'rede_profissional', 'rede_especial', 'slogan', 'concorrentes', 'concorrentes_oferecem', 'missoes',
        'faixa_etaria_social', 'genero', 'quem', 'descricao_clientes', 'encontrar_clientes', 'logotipo_clientes',
        'personalidade', 'outra', 'palavras', 'pessoa', 'caracteristicas', 'cor', 'nao_cor', 'nao_elemento', 'aspectos', 'consideracoes', 'referencias'
        ]
    success_url = reverse_lazy('painel')

    def get_object(self, queryset=None):
        self.object_list = Briefing.objects.get(pk=self.kwargs['pk'], cliente=self.request.user)
        return self.object_list


# View para ver a lista de relatórios do Briefing de Identidade Visual
class RelatorioBriefingView(LoginRequiredMixin, ListView, GroupRequiredMixin):
    model = Briefing
    template_name = 'formularios/relatorio.html'
    group_required = u'Administradores'
    
    def get_queryset(self):

        self.object_list = organizar(Briefing.objects.all())
        return self.object_list


# View para ver o relatório de Briefing de Identidade Visual Detalhadamente
@login_required
def RelatorioBriefingDetalheView(request, pk):
    relatorio = {}
    briefing = Briefing.objects.get(id=pk)
    briefing = (to_dict(briefing))
    print(perguntas)
    for num, resp in enumerate(briefing.values()):
        relatorio[perguntas[num]] = resp
    print(relatorio)
    return render(request, 'formularios/relatorio_detalhe.html', {'relatorio': relatorio})
    
class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('/')


# Tentativa de gerar um arquivo PDF
"""
# Gerar um arquivo PDF com o relatório do Briefing - Identidade Visual
def RelatorioBriefingView(request):
    # Organizando a data
    data_atual = date.today()
    data = data_atual.strftime('%d/%m/%Y')


    # Criar Bytestream buffer
    buf = io.BytesIO()

    # Criar um canvas
    c = canvas.Canvas(buf, pagesize=A4, bottomup=0)

    # Criar um objeto de texto
    textobj = c.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica-Bold", 20)
    textobj.textLine(f"Relatório Briefing Identidade Visual | {data}")
    textobj.textLine("")

    # Designar o model
    briefings = (Briefing.objects.all())

    # Adicionar linhas
    #linhas = []
    linhas = {}

    # Loop
    for briefing in briefings:
        linhas = {
            "titulo": f"{briefing.nome} {briefing.sobrenome} | Briefing Identidade Visual ",
            "Quais os motivos que te levaram a abrir um perfil profissional?": briefing.motivos,
            "Como você vê o seu perfil em 5 anos? E em 10?": briefing.perfil,
            "Seu perfil pode ser outra coisa no futuro ou atuar em outro segmento? Se sim, o que seria?": briefing.segmento,
            "O que te fez me procurar para criar um projeto de Identidade Visual. Por que isso é importante pra você e para seu instagram?": briefing.projeto_identidade,
            "final": " "

        }
        
        linhas.append(f"{briefing.nome} {briefing.sobrenome} | Briefing Identidade Visual")
        linhas.append("Quais os motivos que te levaram a abrir um perfil profissional?")
        linhas.append(briefing.motivos)
        linhas.append("Como você vê o seu perfil em 5 anos? E em 10?")
        linhas.append(briefing.perfil)
        linhas.append("Seu perfil pode ser outra coisa no futuro ou atuar em outro segmento? Se sim, o que seria?")
        linhas.append(briefing.segmento)
        linhas.append(" "*30)

    for pergunta, resposta in linhas.items():
        textobj.setFont("Helvetica-Bold", 14)
        if 'titulo' in pergunta:
            textobj.setFont("Helvetica-Bold", 18)
            textobj.textLine(resposta)
            textobj.textLine("")
        elif 'final' in pergunta:
            textobj.textLine(resposta)
        else:
            textobj.textLine(pergunta)
            textobj.setFont("Helvetica", 14)
            textobj.textLine(resposta)


        




    Tentativa com dicionário
    briefings = (Briefing.objects.all())
    relatorios = []

    for d in briefings:
        briefing = to_dict(d)
        relatorios.append(briefing)

    for dicio in relatorios:
        for q, a in dicio.items():
            print(f'{q}: {a}')


    # Finalizar
    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    # Retornar
    return FileResponse(buf, as_attachment=True, filename="Relatório Briefing.pdf")

"""