# Generated by Django 5.0.4 on 2024-05-18 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=100)),
                ('category_issue', models.CharField(max_length=255)),
                ('category_metric', models.CharField(max_length=100)),
            ],
        ),
    ]
