# Generated by Django 5.2 on 2025-04-23 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'options',
                'managed': False,
            },
        ),
    ]
