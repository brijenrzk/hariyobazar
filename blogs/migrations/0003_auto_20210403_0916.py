# Generated by Django 3.0.1 on 2021-04-03 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20210403_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='title',
            field=models.CharField(max_length=160, null=True, unique=True),
        ),
    ]
