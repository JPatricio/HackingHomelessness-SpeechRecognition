# Generated by Django 2.1.7 on 2019-02-24 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fanhanhas', '0004_remove_report_topics'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='topics',
            field=models.CharField(default='counsil;drugs;bills;gym', max_length=300),
            preserve_default=False,
        ),
    ]