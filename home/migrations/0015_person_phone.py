# Generated by Django 2.2.7 on 2019-12-08 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_careerpage_careersindexpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]