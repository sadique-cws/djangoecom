# Generated by Django 3.0.7 on 2020-06-26 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200626_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
