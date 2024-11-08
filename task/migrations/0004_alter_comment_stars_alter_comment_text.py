# Generated by Django 4.2.2 on 2024-11-06 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_task_options_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='stars',
            field=models.CharField(choices=[('BIR', 'BIR'), ('IKKI', 'IKKI'), ('UCH', 'UCH'), ('TORT', 'TORT'), ('BESH', 'BESH')], max_length=5, verbose_name='Yulduzchalar'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Izoh'),
        ),
    ]
