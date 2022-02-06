from .models import Briefing
from allauth.account.forms import SignupForm
from django import forms
 
 
# Formulário de Cadastro é modificado, para ser colocado também o Nome e Sobrenome
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, label='Nome')
    last_name = forms.CharField(max_length=75, label='Sobrenome')
 
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # Salva o Usuário (username) como o nome completo, porém, os espaços são trocados por '_', pois Usuário não pode ter espaço
        user.username = (f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}")
        user.username = user.username.replace(" ", "_")
        # Salva o usuário
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

# Formulário do Briefing de Identidade Visual
class BriefingForm(forms.ModelForm):
    class Meta:
        model = Briefing
        fields = (
        'nome', 'sobrenome', 'motivos', 'perfil', 'segmento', 'projeto_identidade', 'conta_profissional',
        'rede_social', 'rede_profissional', 'rede_especial', 'slogan', 'concorrentes', 'concorrentes_oferecem', 'missoes',
        'faixa_etaria_social', 'genero', 'quem', 'descricao_clientes', 'encontrar_clientes', 'logotipo_clientes',
        'personalidade', 'outra', 'palavras', 'pessoa', 'caracteristicas', 'cor', 'nao_cor', 'nao_elemento', 'aspectos', 'consideracoes', 'referencias'
        )