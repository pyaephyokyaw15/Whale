# Generated by Django 4.0.6 on 2022-07-13 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='authentic',
            field=models.BooleanField(default=False),
        ),
    ]
