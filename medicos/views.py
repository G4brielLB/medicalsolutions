from distutils.log import Log
import imp
from tokenize import group
from urllib import request
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from allauth.account.views import LoginView
from .models import Foto, Video, Calendario, Briefing, organizar, to_dict, perguntas
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from datetime import date
from allauth.account.views import PasswordChangeView
from .forms import BriefingForm
from django.http import HttpRequest

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.lib.pagesizes import A4
from itertools import chain





app_name = "medicos"

# Create your views here.

def PaginaInicial(request):
    return render(request, 'index.html')

#@login_required
#def Painel(request):
#    return render(request, "painel.html")



class Painel(LoginRequiredMixin, ListView):
    model = Briefing
    template_name = "painel.html"

    def get_queryset(self):

        self.object_list = Briefing.objects.filter(cliente=self.request.user)
        print(self.request.user)
        print(Briefing.objects.filter(cliente=self.request.user))
        return self.object_list

@login_required
def Posts(request):
    return render(request, "posts/postagens.html")

class FotosView(LoginRequiredMixin, ListView):
    model = Foto
    template_name = "posts/fotos.html"

    def get_queryset(self):

        self.object_list = Foto.objects.filter(cliente=self.request.user)
        return self.object_list

@login_required
def viewFoto(request, pk):
    foto = Foto.objects.get(id=pk)
    all = (Foto.objects.filter(cliente=request.user))
    filtro = list(all)
    if foto in filtro:
        return render(request, 'posts/foto.html', {'foto': foto})
    else:
        return render(request, 'posts/indisponivel.html')



class VideosView(LoginRequiredMixin, ListView):
    model = Video
    template_name = "posts/videos.html"

    def get_queryset(self):

        self.object_list = Video.objects.filter(cliente=self.request.user)
        return self.object_list


@login_required
def viewVideo(request, pk):
    video = Video.objects.get(id=pk)
    all = (Video.objects.filter(cliente=request.user))
    filtro = list(all)
    print(filtro)
    if video in filtro:
        return render(request, 'posts/video.html', {'video': video})
    else:
        return render(request, 'posts/indisponivel.html')


class CalendarioView(LoginRequiredMixin, ListView):
    model = Calendario
    template_name = "calendario/calendario.html"

    def get_queryset(self):

        self.object_list = Calendario.objects.filter(cliente=self.request.user)
        return self.object_list


class EditarPerfilView(UpdateView, LoginRequiredMixin):
    model = User
    template_name = 'account/perfil.html'
    fields = ["first_name", "last_name", "email"]
    success_url = reverse_lazy('painel')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(User, username=self.request.user)
        return self.object


class EditarSenhaView(PasswordChangeView, LoginRequiredMixin):
    form_class = PasswordChangeForm
    template_name = 'account/senha.html'
    success_url = reverse_lazy('painel')


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
@login_required
def BriefingView(request):
    if request.method == 'POST':
        form = BriefingForm(data=request.POST)
        if form.is_valid():
            form.save()
            briefing = form.save(commit=False) 
            briefing.cliente = request.user # the user must be logged in for this.
            briefing.save()
        return redirect('painel')
    else:
        form = BriefingForm()

    return render(request, 'formularios/briefing.html', {"form": form})


class BriefingUpdateView(LoginRequiredMixin, UpdateView):
    model = Briefing
    template_name = 'formularios/briefing.html'
    fields = [
        'nome', 'sobrenome', 'motivos', 'perfil', 'segmento', 'projeto_identidade', 'conta_profissional',
        'rede_social', 'rede_profissional', 'rede_especial', 'slogan', 'concorrentes', 'concorrentes_oferecem', 'missoes',
        'faixa_etaria_social', 'genero', 'quem', 'descricao_clientes', 'encontrar_clientes', 'logotipo_clientes',
        'personalidade', 'palavras', 'pessoa', 'caracteristicas', 'cor', 'nao_cor', 'nao_elemento', 'aspectos', 'consideracoes', 'referencias'
        ]
    success_url = reverse_lazy('painel')

    def get_object(self, queryset=None):
        self.object_list = Briefing.objects.get(pk=self.kwargs['pk'], cliente=self.request.user)
        return self.object_list


class RelatorioBriefingView(LoginRequiredMixin, ListView, GroupRequiredMixin):
    model = Briefing
    template_name = 'formularios/relatorio.html'
    group_required = u'Administradores'
    
    def get_queryset(self):

        self.object_list = organizar(Briefing.objects.all())
        return self.object_list

#class RelatorioBriefingDetalheView(DetailView):
 #   model = Briefing
 #   template_name = 'formularios/relatorio_detalhe.html'

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