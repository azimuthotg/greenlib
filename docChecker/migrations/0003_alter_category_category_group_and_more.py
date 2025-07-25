# Generated by Django 5.0.6 on 2024-12-02 02:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docChecker', '0002_evidence_created_at_evidence_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='docChecker.categorygroup'),
        ),
        migrations.AlterField(
            model_name='categorygroup',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_groups', to='docChecker.year'),
        ),
        migrations.AlterField(
            model_name='evidence',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidences', to='docChecker.indicator'),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicators', to='docChecker.issue'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='docChecker.category'),
        ),
    ]
