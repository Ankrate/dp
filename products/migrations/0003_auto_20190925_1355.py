# Generated by Django 2.2.1 on 2019-09-25 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190916_0746'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='img_check',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='products',
            name='main_img',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]