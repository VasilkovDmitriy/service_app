# Generated by Django 4.1.7 on 2023-04-30 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_subscription_unique_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='comment',
            field=models.CharField(default='', max_length=50),
        ),
    ]