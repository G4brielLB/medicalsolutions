from django.urls import path
from django.contrib.auth import views as auth_views

#Importa as Views criadas
from .views import (BriefingUpdateView, CalendarioView, EditarPerfilView, EditarSenhaView, PaginaInicial,
Painel, FotosView, Posts, BriefingView, RelatorioBriefingDetalheView,
VideosView, FormulariosView, RelatorioBriefingView, RelatorioBriefingDetalheView,
viewVideo, BriefingUpdateView, CustomPasswordChangeView)
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.PaginaInicial, name='index'),
    path('painel', Painel.as_view(), name='painel'),
    path('posts', views.Posts, name='posts'),
    path('posts/fotos', FotosView.as_view(), name='fotos'),
    path('posts/fotos/<int:pk>', views.viewFoto, name='foto'),
    path('posts/videos', VideosView.as_view(), name='videos'),
    path('posts/videos/<int:pk>', views.viewVideo, name='video'),
    path('calendario', CalendarioView.as_view(), name='calendario'),
    path('formularios', FormulariosView.as_view(), name='formularios'),
    path('formularios/briefing', views.BriefingView, name='briefing'),
    path('formularios/briefing/editar/<int:pk>', BriefingUpdateView.as_view(), name='editar_briefing'),
    path('relatorio/briefing', RelatorioBriefingView.as_view(), name='relatorio_briefing' ),
    path('relatorio/briefing/<int:pk>', views.RelatorioBriefingDetalheView, name='relatorio_detalhe'),
    path('editar/perfil', EditarSenhaView.as_view(), name='editar_senha'),
    #path("editar/perfil/", auth_views.PasswordChangeView.as_view(template_name='account/senha.html'), name="editar_senha"),
    path("editar/senha/", EditarPerfilView.as_view(), name='editar_perfil')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)