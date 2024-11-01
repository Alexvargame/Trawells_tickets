# Generated by Django 4.1.7 on 2023-07-04 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railway', '0029_scheduletrains_time_train'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='on_sale',
        ),
        migrations.AddField(
            model_name='ticket',
            name='booked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='scheduletrains',
            name='time_train',
            field=models.TimeField(verbose_name='Время'),
        ),
    ]
