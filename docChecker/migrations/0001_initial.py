# Generated by Django 5.0.4 on 2024-05-26 05:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryGroup',
            fields=[
                ('category_group_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=255)),
                ('group_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('indicator_id', models.AutoField(primary_key=True, serialize=False)),
                ('indicator_name', models.CharField(max_length=255)),
                ('indicator_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('year_id', models.AutoField(primary_key=True, serialize=False)),
                ('year_name', models.CharField(max_length=255)),
                ('year_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255)),
                ('category_description', models.TextField()),
                ('category_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docChecker.categorygroup')),
            ],
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('evidence_id', models.AutoField(primary_key=True, serialize=False)),
                ('evidence_name', models.CharField(max_length=255)),
                ('evidence_description', models.TextField()),
                ('evidence_file', models.FileField(upload_to='evidence/')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docChecker.indicator')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('issue_id', models.AutoField(primary_key=True, serialize=False)),
                ('issue_name', models.CharField(max_length=255)),
                ('issue_description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docChecker.category')),
            ],
        ),
        migrations.AddField(
            model_name='indicator',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docChecker.issue'),
        ),
        migrations.AddField(
            model_name='categorygroup',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docChecker.year'),
        ),
    ]