# Generated by Django 3.2.6 on 2021-12-06 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_auto_20211113_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imagepresent',
            field=models.ImageField(default=None, upload_to='media'),
        ),
    ]
