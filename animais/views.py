from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView
from django.utils import timezone as tz

from io import BytesIO
from PIL import Image
from os import environ as env
import os
import supabase

from .models import Animal, Doacao
from .forms import AnimalForm

if os.path.isfile('./.env'):
    from loadenv import load_env_file
    load_env_file()

SUPABASE_IMAGES_BUCKET_NAME = env.get("SUPABASE_IMAGES_BUCKET_NAME")
SUPABASE_URL = env.get("SUPABASE_URL")
SUPABASE_KEY = env.get("SUPABASE_API_KEY")

class IndexView(ListView):
    template_name = "animais/index.html"
    paginate_by = 6
    model = Animal

    def get_queryset(self):
        return Animal.objects.order_by("-adicionado_em")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Paginator(self.get_queryset(), self.paginate_by)
        context['num_pages'] = context['paginator'].num_pages
        return context

class SobreView(TemplateView):
    template_name = 'animais/sobre.html'

def cadastro(request):
    if not request.method == 'POST':
        request.session['next'] = request.path
        form = AnimalForm()
        return render(request, 'animais/cadastro.html', {'form': form})

    form = AnimalForm(request.POST, request.FILES)
    if form.is_valid():
        animal = form.save(commit=False)
        data_hora = \
            tz.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z").replace(" ", "_")
        path_on_supabase = f'animal_{data_hora}.jpg'
        if 'arquivo_imagem' in request.FILES:
            imagem = request.FILES['arquivo_imagem'].read()
            imagem_reduzida = redimensionar_imagem(
                imagem=imagem, largura_maxima=1366, altura_maxima=768)
            client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
            response = \
                client.storage.from_(SUPABASE_IMAGES_BUCKET_NAME).upload(
                    file=imagem_reduzida,
                    path=path_on_supabase,
                    file_options={"content-type": "image/jpeg"},
                )
            if response.status_code == 200:
                animal.imagem = "{}/storage/v1/object/public/{}/{}".format(
                    SUPABASE_URL,
                    SUPABASE_IMAGES_BUCKET_NAME,
                    path_on_supabase,
                )
                animal.adicionado_por = request.user.username
                animal.save()
                request.session['new_animal_id'] = animal.id
                return redirect('animais:cadastro_sucesso')
    return render(request, 'animais/cadastro.html', {'form': form})

def cadastro_sucesso(request):
    animal_id = request.session.get('new_animal_id', None)
    if animal_id is not None:
        animal = get_object_or_404(Animal, id=animal_id)
        return render(
            request, 'animais/cadastro_sucesso.html', {'animal': animal})
    return render(request, 'animais/cadastro_sucesso.html', {'animal': None})

def redimensionar_imagem(imagem, largura_maxima, altura_maxima):
    img = Image.open(BytesIO(imagem))
    img = img.convert('RGB')
    largura_original, altura_original = img.size
    nova_largura, nova_altura = largura_original, altura_original
    while nova_altura > altura_maxima or nova_largura > largura_maxima:
        if nova_altura > altura_maxima:
            nova_altura = altura_maxima
            nova_largura = \
                int((largura_original / altura_original) * nova_altura)
        if nova_largura > largura_maxima:
            nova_largura = largura_maxima
            nova_altura = \
                int((altura_original / largura_original) * nova_largura)
    img = img.resize((nova_largura, nova_altura))
    buffer = BytesIO()
    img.save(buffer, 'JPEG')
    return buffer.getvalue()

def login_admin(request):
    error_message = ""
    if request.method == "POST":
        print("request.session.get('next'):", request.session.get('next'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = authenticate(request, username=username, password=password)
        if admin is not None:
            login(request, admin)
            next_page = request.session.get('next') or '/'
            return redirect(next_page)
        else:
            error_message = "Login e/ou senha inválido(s)."
    if error_message:
        return render(request, 'animais/login.html',
            {'error_message': error_message})
    return render(request, 'animais/login.html')

def logout_admin(request):
    logout(request)
    return redirect('/')

def registro_doacao(request):
    data = {}

    data['doacoes'] = Doacao.objects.all()

    print(data['doacoes'][0])

    if request.method == "POST":
        tipo_doacao = request.POST.get('tipo_doacao')
        quantidade  = request.POST.get('quantidade')
        unidade     = request.POST.get('unidade')
        postdate    = request.POST.get('postdate')


        try:
            doacao = Doacao(
                tipo_doacao = tipo_doacao,
                quantidade = quantidade,
                unidade = unidade,
                data_registro = postdate
            )

            doacao.save()

            data['aviso'] = f"Cadastro de {quantidade} {unidade} {tipo_doacao} em {postdate} realizado com sucesso."
            data['alert_type'] = 'alert-primary'
        except:
            data['aviso'] = f"Erro ao cadastrar {quantidade} {unidade} {tipo_doacao} em {postdate}."
            data['alert_type'] = 'alert-danger'


    return render(request, 'animais/registro_doacao.html', data)

