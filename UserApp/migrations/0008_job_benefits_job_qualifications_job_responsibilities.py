# Generated by Django 4.2.5 on 2023-09-16 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0007_alter_job_options_job_job_type_job_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='benefits',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='qualifications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='responsibilities',
            field=models.TextField(blank=True, null=True),
        ),
    ]