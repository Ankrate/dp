# Generated by Django 2.2.1 on 2019-09-11 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20190911_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='cat_n',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='products',
            name='seller',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
