# Generated by Django 4.1.6 on 2023-08-13 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='women',
            old_name='cat',
            new_name='cat_slug',
        ),
    ]
