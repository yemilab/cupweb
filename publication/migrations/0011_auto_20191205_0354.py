# Generated by Django 2.2.7 on 2019-12-05 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('publication', '0010_auto_20191205_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperpage',
            name='cover_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='paperpage',
            name='is_featured',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presentationpage',
            name='cover_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='presentationpage',
            name='is_featured',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
