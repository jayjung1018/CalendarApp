# Generated by Django 2.0.5 on 2018-07-19 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='name',
            new_name='title',
        ),
    ]
