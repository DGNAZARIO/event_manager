# Generated by Django 5.1.2 on 2024-11-16 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_evento_organizador_registration'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='status',
            field=models.CharField(default='pendente', max_length=50),
            preserve_default=False,
        ),
    ]