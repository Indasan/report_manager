# Generated by Django 3.2.2 on 2021-05-06 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csv',
            old_name='creatred',
            new_name='created',
        ),
    ]
