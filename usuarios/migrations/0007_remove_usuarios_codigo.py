# Generated by Django 4.2.2 on 2023-07-11 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_alter_usuarios_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='codigo',
        ),
    ]
