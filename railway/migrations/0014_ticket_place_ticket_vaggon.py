# Generated by Django 4.1.7 on 2023-06-26 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railway', '0013_ticket_on_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='place',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='ticket',
            name='vaggon',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]