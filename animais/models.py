from django.core import validators
from django.core.files import File
from django.db import models
from django.utils import timezone as tz
import datetime as dt


class Animal(models.Model):
    def __str__(self):
        return "{} ({}/{}) incluído em: {}".format(
            self.nome,
            self.especie,
            self.sexo,
            self.adicionado_em,
        )

    def validate_nome(value):
        if not any(char.isalpha() for char in value):
            raise validators.ValidationError(
                "O campo nome deve conter pelo menos uma letra.")

    # nome
    nome = models.CharField(
        max_length=100,
        validators=[validate_nome],
        blank=False,
        null=False,
    )

    ESPECIE_CHOICES = (
        ('c', 'cachorro'),
        ('g', 'gato'),
        ('o', 'outro'),
    )
    # especie
    especie = models.CharField(
        max_length=8,
        verbose_name='espécie',
        choices=ESPECIE_CHOICES,
        blank=False,
        null=False,
    )

    SEXO_CHOICES = (
        ('m', 'macho'),
        ('f', 'fêmea'),
    )
    # sexo
    sexo = models.CharField(
        max_length=5,
        choices=SEXO_CHOICES,
        blank=False,
        null=False,
    )

    # imagem
    imagem = models.URLField(blank=False, null=False)

    # adicionado_em
    adicionado_em = models.DateTimeField(auto_now_add=True)

    # adicionado_por
    adicionado_por = models.CharField(max_length=100)

class Tipo_Doacao(models.Model):

    def __str__(self):
        return f"{self.nome} ({self.unidade})"

    nome    = models.CharField(max_length = 20)
    unidade = models.CharField(max_length = 20)


class Doacao(models.Model):
    def __str__(self):
        return f"{self.quantidade}  de {self.tipo_doacao.nome} em {self.data_registro}"

    tipo_doacao   = models.ForeignKey(Tipo_Doacao, on_delete = models.CASCADE)
    quantidade    = models.IntegerField()
    data_registro = models.DateField()


class Meta(models.Model):
    def __str__(self):
        return f"{self.meta_mensal}  de {self.tipo_doacao.nome} definida em {self.data_registro}"

    tipo_doacao   = models.ForeignKey(Tipo_Doacao, on_delete = models.CASCADE)
    meta_mensal   = models.IntegerField()
    data_registro = models.DateField()

    class Meta:
        unique_together = ('data_registro', 'tipo_doacao')