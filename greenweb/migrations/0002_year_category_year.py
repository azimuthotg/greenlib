# Generated by Django 5.0.4 on 2024-05-25 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('year', models.IntegerField(primary_key=True, serialize=False, verbose_name='ปี')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='year',
            field=models.ForeignKey(default=2024, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='greenweb.year', verbose_name='ปี'),
        ),
    ]
