# Generated by Django 2.0.5 on 2018-05-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180527_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='number',
            field=models.IntegerField(default=0, verbose_name='标签数目'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='number',
            field=models.IntegerField(default=0, verbose_name='标签数目'),
        ),
    ]