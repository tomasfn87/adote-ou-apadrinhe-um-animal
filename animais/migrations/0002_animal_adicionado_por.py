# Generated by Django 4.2.6 on 2024-03-23 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animais', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='adicionado_por',
            field=models.CharField(default='admin', max_length=100),
            preserve_default=False,
        ),
    ]
