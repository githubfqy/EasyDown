# Generated by Django 2.0.5 on 2018-05-30 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_article_article_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['content'], 'verbose_name': '留言板', 'verbose_name_plural': '留言板'},
        ),
        migrations.AlterModelTable(
            name='message',
            table='Message',
        ),
    ]
