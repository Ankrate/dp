# Generated by Django 2.2.1 on 2019-09-11 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20190911_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='car',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
