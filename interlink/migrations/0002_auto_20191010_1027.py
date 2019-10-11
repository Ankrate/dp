# Generated by Django 2.2.1 on 2019-10-10 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interlink', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedirectProductOldToNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('id_new', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'redirect_product_old_to_new',
                'managed': True,
            },
        ),
        migrations.RenameModel(
            old_name='Tableredirectcat',
            new_name='RedireCtcat',
        ),
        migrations.AlterModelOptions(
            name='redirectcat',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='redirectcat',
            table='redirect_cat',
        ),
    ]