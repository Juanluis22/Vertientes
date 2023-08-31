# Generated by Django 4.2.4 on 2023-08-24 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comunidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('vertientes', models.PositiveIntegerField(default=0)),
                ('ubicación', models.CharField(max_length=200, verbose_name='Ubicación')),
            ],
            options={
                'verbose_name': 'Comunidad',
                'verbose_name_plural': 'Comunidades',
                'db_table': 'comunidad',
                'ordering': ['id'],
            },
        ),
    ]
