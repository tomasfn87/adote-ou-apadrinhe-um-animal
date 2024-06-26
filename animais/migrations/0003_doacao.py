# Generated by Django 4.2.6 on 2024-03-26 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animais', '0002_animal_adicionado_por'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_doacao', models.CharField(max_length=20)),
                ('quantidade', models.IntegerField()),
                ('unidade', models.CharField(choices=[('k', 'Kg'), ('g', 'Gramas'), ('u', 'Unidades')], max_length=10)),
                ('data_registro', models.DateField()),
            ],
        ),
    ]
