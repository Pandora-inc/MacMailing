# Generated by Django 4.1.3 on 2024-07-02 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliares', '0003_currency_type_code_alter_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='code',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]