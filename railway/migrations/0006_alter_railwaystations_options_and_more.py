# Generated by Django 4.1.7 on 2023-06-07 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('railway', '0005_railwaystations_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='railwaystations',
            options={'default_related_name': 'railwaystations', 'verbose_name': 'Вокзал', 'verbose_name_plural': 'Вокзалы'},
        ),
        migrations.AlterField(
            model_name='railwaystations',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city', to='railway.cities', verbose_name='Город'),
        ),
    ]
