# Generated by Django 5.1 on 2024-09-10 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_advancedprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='advancedprofile',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
