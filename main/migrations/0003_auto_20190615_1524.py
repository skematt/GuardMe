# Generated by Django 2.2 on 2019-06-15 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190615_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crime',
            name='reported_date',
            field=models.DateField(auto_now=True),
        ),
    ]
