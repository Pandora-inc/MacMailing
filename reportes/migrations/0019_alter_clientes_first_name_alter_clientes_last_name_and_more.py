# Generated by Django 4.1.3 on 2024-07-09 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0018_mailstosend_order_alter_clientes_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='first_name',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='last_name',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='lead_name',
            field=models.CharField(max_length=64),
        ),
    ]
