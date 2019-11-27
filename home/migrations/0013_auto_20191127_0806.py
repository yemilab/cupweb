# Generated by Django 2.2.7 on 2019-11-27 08:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('home', '0012_auto_20191124_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeslider',
            name='date_published',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Published date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homeslider',
            name='description',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='homeslider',
            name='related_page',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.Page'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homeslider',
            name='subtitle',
            field=models.CharField(default=' ', max_length=250),
            preserve_default=False,
        ),
    ]