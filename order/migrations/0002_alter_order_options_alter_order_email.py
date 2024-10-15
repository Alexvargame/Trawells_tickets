# Generated by Django 4.1.7 on 2023-06-26 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created',), 'verbose_name': 'Покупатель', 'verbose_name_plural': 'Покупатели'},
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]