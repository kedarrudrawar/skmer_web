# Generated by Django 2.2.1 on 2019-05-24 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RefLibrary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='reference_lib/')),
            ],
        ),
    ]
