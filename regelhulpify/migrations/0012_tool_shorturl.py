# Generated by Django 3.1.1 on 2020-11-05 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regelhulpify', '0011_tool_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='shorturl',
            field=models.SlugField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
