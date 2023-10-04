# Generated by Django 4.2.4 on 2023-10-03 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0007_vertiente_latitud_vertiente_longitud'),
        ('user', '0008_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='comunidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nucleo.comunidad'),
        ),
    ]