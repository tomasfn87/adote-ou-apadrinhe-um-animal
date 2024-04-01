from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView
from django.utils import timezone as tz
from django.contrib import messages
from django.db import IntegrityError , connection
from django.db.models.functions import TruncMonth
from django.db.models import Sum

from io import BytesIO
from PIL import Image
from os import environ as env
import os
import supabase

from .models import Animal, Doacao, Tipo_Doacao, Meta
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = authenticate(request, username=username, password=password)
        if admin is not None:
            login(request, admin)
            next_page = request.session.get('next', '/')
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


    data['tipo_doacao'] = Tipo_Doacao.objects.all()

    if request.method == "POST":

        try:
            doacao = Doacao.objects.create(
                tipo_doacao_id = request.POST.get('tipo_doacao'),
                quantidade     = request.POST.get('quantidade'),
                data_registro  = request.POST.get('postdate')
            )

            messages.success(request, f"Sucesso: Cadastro de {doacao.quantidade} {doacao.tipo_doacao.unidade} de {doacao.tipo_doacao.nome} em {doacao.data_registro}.")
        except Exception as e:
            messages.warning(request, f"Erro ao adicionar Meta")

    data['doacoes'] = Doacao.objects.all()[::-1]

    return render(request, 'animais/registro_doacao.html', data)


def delete_doacao(request, doacao_id):
    doacao = get_object_or_404(Doacao, pk=doacao_id)
    if request.method == 'POST':
        doacao.delete()
    return redirect('animais:registro_doacao')

def metas(request):
    data = {}

    if request.method =="POST":
        post = request.POST

        try:
            data_registro = f"{post.get('ano_meta')}-{post.get('mes_meta')}-1"

            meta = Meta.objects.create(
                tipo_doacao_id=post.get('tipo_doacao'),
                meta_mensal=post.get('meta_mensal'),
                data_registro=data_registro
            )
            messages.success(request ,f"Meta de {meta.tipo_doacao.nome} Adicionada com sucesso")

        except IntegrityError:
            messages.warning(request, "Erro: Já existe meta para esse tipo e mes")

        except Exception as e:
            messages.warning(request, f"Erro ao adicionar Meta")

    data['tipo_doacao'] = Tipo_Doacao.objects.all()
    data['metas']       = Meta.objects.all()[::-1]

    return render(request, 'animais/metas.html', data)


def delete_meta(request, meta_id):
    meta = get_object_or_404(Meta, pk=meta_id)
    if request.method == 'POST':
        meta.delete()
    return redirect('animais:metas')


def status_meta(request):
    data_meta = request.GET.get('escolha_data')
    if data_meta == None:
        data_meta = tz.now().strftime("%Y-%m-%d")

    print(data_meta)


    data = {}

    cursor = connection.cursor()
    #entender por que precisei colocar + 1 month


    cursor.execute(f'''
                    with dates as 
                    (select distinct a.date_trunc from
                            (select date_trunc('month', data_registro) from animais_doacao
                            union all
                            select date_trunc('month', data_registro) from animais_meta) a
                    ),
                    totais as
                    (
                            select 
                                    date_trunc('month',data_registro) data_totais, 
                                    tipo_doacao_id, 
                                    sum(quantidade) total 
                            from 
                                    animais_doacao 
                            group by 1,2
                    ),
                    metas as 
                    (
                    select 
                            tipo_doacao_id,
                            data_registro,
                            coalesce(lead(data_registro) over (partition by tipo_doacao_id order by data_registro), '2050-01-01') to_date,
                            meta_mensal
                      from 
                            animais_meta
                    ) 
                    
                    select
                            nome,
                            d.date_trunc+ interval '1 day' as data_ref,
                            coalesce(total, 0) total,
                            coalesce(meta_mensal, 0) meta,
                            100*coalesce(t.total, 0) / NULLIF(m.meta_mensal,0) as percent
                    from 
                            dates d
                    cross join
                            animais_tipo_doacao atd
                    left join totais t
                    on      t.data_totais = d.date_trunc
                    and     t.tipo_doacao_id = atd.id
                    left join metas m
                    on      d.date_trunc >= m.data_registro
                    and     d.date_trunc <  m.to_date
                    and     m.tipo_doacao_id = atd.id;
                    ''')


    row = cursor.fetchall()

    response = {}
    products = {x[0] for x in row}

    for p in products:
        response[p] = []

    for r in row:
        p = r[0]

        response[p].append(
            (r[1],r[2],r[3],r[4])
        )

    print(response)
    data['resp'] = response

    data['query']=row

    data['dist_datas']  = list({ x[1] for x in row } )

    #print(data['values'])

    return render(request, 'animais/status_meta.html', data)
