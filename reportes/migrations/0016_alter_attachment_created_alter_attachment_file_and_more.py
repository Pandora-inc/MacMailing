# Generated by Django 4.1.3 on 2024-07-05 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0015_alter_templatefiles_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to='attachments/'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='templatefiles',
            name='template_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reportes.templatesgroup'),
        ),
        migrations.AlterUniqueTogether(
            name='templatefiles',
            unique_together={('orden', 'template_group')},
        ),
    ]
