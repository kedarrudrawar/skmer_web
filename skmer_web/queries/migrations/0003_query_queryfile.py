# Generated by Django 2.2.1 on 2019-05-31 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0002_auto_20190525_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='queryFile',
            field=models.FileField(default=None, upload_to='queryFiles/'),
        ),
    ]
