# Generated by Django 5.1.4 on 2025-01-11 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0002_alter_action_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='alert',
            field=models.BooleanField(default=False),
        ),
    ]