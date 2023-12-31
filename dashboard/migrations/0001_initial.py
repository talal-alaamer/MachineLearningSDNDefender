# Generated by Django 4.1.13 on 2023-12-18 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaptureLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('action', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'CaptureLog',
            },
        ),
    ]
