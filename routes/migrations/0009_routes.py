# Generated by Django 4.1.7 on 2023-06-05 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('railway', '0005_railwaystations_status'),
        ('routes', '0008_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finish', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='routefinishpoint', to='railway.railwaystations', verbose_name='Конечный пункт')),
                ('start', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='routestartpoint', to='railway.railwaystations', verbose_name='Начальный пункт')),
                ('stations_distance', models.ManyToManyField(blank=True, related_name='distances', to='routes.neighboursdistance', verbose_name='расстояния')),
            ],
            options={
                'verbose_name': 'Маршрут',
                'verbose_name_plural': 'Маршруты',
            },
        ),
    ]