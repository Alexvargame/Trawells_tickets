# Generated by Django 4.1.7 on 2023-06-01 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_alter_neighboursdistance_finish_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NeighboursDistance',
        ),
    ]
