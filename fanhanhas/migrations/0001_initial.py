# Generated by Django 2.1.7 on 2019-02-23 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now=True)),
                ('transcript', models.TextField()),
            ],
        ),
    ]