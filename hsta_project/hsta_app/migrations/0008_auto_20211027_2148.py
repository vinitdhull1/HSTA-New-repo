# Generated by Django 3.2 on 2021-10-27 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsta_app', '0007_hstadata_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hstadata',
            name='ISBN',
            field=models.CharField(blank=True, max_length=10000000),
        ),
        migrations.AlterField(
            model_name='hstadata',
            name='author',
            field=models.CharField(blank=True, max_length=10000000),
        ),
        migrations.AlterField(
            model_name='hstadata',
            name='chapter',
            field=models.CharField(blank=True, max_length=10000000),
        ),
        migrations.AlterField(
            model_name='hstadata',
            name='title',
            field=models.CharField(blank=True, max_length=10000000),
        ),
        migrations.AlterField(
            model_name='hstadata',
            name='zip_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
