# Generated by Django 3.1.1 on 2020-10-14 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regelhulpify', '0007_auto_20201014_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='nextquestion',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='comesfrom', to='regelhulpify.question'),
        ),
    ]
