# Generated by Django 4.1.3 on 2024-05-07 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0008_mailstosend_error_message_mailstosend_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailstosend',
            name='mail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reportes.mail'),
        ),
    ]
