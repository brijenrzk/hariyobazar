# Generated by Django 3.0.1 on 2020-10-19 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='contact',
            field=models.BigIntegerField(null=True),
        ),
    ]