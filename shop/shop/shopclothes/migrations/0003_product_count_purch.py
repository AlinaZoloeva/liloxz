# Generated by Django 4.1.6 on 2024-01-24 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopclothes', '0002_alter_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count_purch',
            field=models.IntegerField(default=0),
        ),
    ]