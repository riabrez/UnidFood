# Generated by Django 2.2.3 on 2025-03-26 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unidfood', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
    ]
