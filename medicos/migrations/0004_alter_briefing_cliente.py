# Generated by Django 4.0.1 on 2022-01-19 16:56

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medicos', '0003_alter_briefing_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='briefing',
            name='cliente',
            field=models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
