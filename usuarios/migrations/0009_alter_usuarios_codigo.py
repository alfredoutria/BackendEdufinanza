# Generated by Django 4.2.2 on 2023-07-11 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_usuarios_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='codigo',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]