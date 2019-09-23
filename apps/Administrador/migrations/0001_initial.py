# Generated by Django 2.2.4 on 2019-09-22 03:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('nombres', models.CharField(max_length=40)),
                ('apellido_paterno', models.CharField(max_length=30)),
                ('apellido_materno', models.CharField(max_length=30)),
                ('celular', models.CharField(blank=True, max_length=12)),
                ('telefono', models.CharField(blank=True, max_length=9)),
                ('direccion', models.CharField(blank=True, max_length=90)),
                ('fechaReg', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('estReg', models.BooleanField(default=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Administrador.Area')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Administrador.Especialidad')),
                ('tipo_personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Administrador.TipoPersonal')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
