# Generated by Django 4.1.3 on 2024-05-08 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0009_alter_mailstosend_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
