# Generated by Django 3.2.6 on 2021-12-15 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_detailorder_israting'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Ingredient',
            field=models.TextField(blank=True, null=True),
        ),
    ]