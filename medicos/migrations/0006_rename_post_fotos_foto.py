# Generated by Django 4.0.1 on 2022-01-20 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0005_fotos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fotos',
            old_name='post',
            new_name='foto',
        ),
    ]
