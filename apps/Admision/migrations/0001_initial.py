# Generated by Django 2.2.4 on 2019-09-19 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Administrador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GrupSang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HorarioCab',
            fields=[
                ('codigoHor', models.AutoField(primary_key=True, serialize=False)),
                ('dias', models.IntegerField(blank=True, null=True)),
                ('turno', models.IntegerField(blank=True, null=True)),
                ('fechaInicio', models.DateTimeField(blank=True, null=True)),
                ('fechaFin', models.DateTimeField(blank=True, null=True)),
                ('personal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Administrador.Personal')),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HorarioDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(max_length=12)),
                ('hora_inicio', models.DateTimeField(null=True)),
                ('hora_fin', models.DateTimeField(null=True)),
                ('codigoHor', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='Admision.HorarioCab')),
            ],
        ),
        migrations.CreateModel(
            name='Historia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroHistoria', models.IntegerField()),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('nombres', models.CharField(max_length=30)),
                ('apellido_paterno', models.CharField(max_length=30)),
                ('apellido_materno', models.CharField(max_length=30)),
                ('sexo', models.CharField(max_length=10)),
                ('edad', models.IntegerField(null=True)),
                ('fechaNac', models.DateField(blank=True, null=True)),
                ('foto', models.BinaryField(blank=True, null=True)),
                ('celular', models.CharField(blank=True, max_length=10, null=True)),
                ('telefono', models.CharField(blank=True, max_length=9, null=True)),
                ('estadoCivil', models.CharField(blank=True, max_length=15, null=True)),
                ('gradoInstruccion', models.CharField(blank=True, max_length=15, null=True)),
                ('ocupacion', models.CharField(blank=True, max_length=30, null=True)),
                ('fechaReg', models.DateField(auto_now_add=True)),
                ('direccion', models.CharField(blank=True, max_length=90, null=True)),
                ('nacionalidad', models.CharField(blank=True, max_length=30, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('estReg', models.BooleanField(default=True)),
                ('departamento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Admision.Departamento')),
                ('distrito', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Admision.Distrito')),
                ('grupoSanguineo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Admision.GrupSang')),
                ('provincia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Admision.Provincia')),
            ],
        ),
    ]
