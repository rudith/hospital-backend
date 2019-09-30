# Generated by Django 2.2.4 on 2019-09-30 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExamenLabCab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=8)),
                ('orden', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha', models.DateField()),
                ('observaciones', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoExamen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ExamenLabDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
                ('resultado_obtenido', models.TextField()),
                ('unidades', models.CharField(blank=True, max_length=100, null=True)),
                ('rango_referencia', models.CharField(max_length=100)),
                ('codigoExam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='Laboratorio.ExamenLabCab')),
            ],
        ),
        migrations.AddField(
            model_name='examenlabcab',
            name='tipoExam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Laboratorio.TipoExamen'),
        ),
    ]
