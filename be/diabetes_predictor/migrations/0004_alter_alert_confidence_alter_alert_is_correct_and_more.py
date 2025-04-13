# Generated by Django 4.2.10 on 2025-04-13 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diabetes_predictor', '0003_delete_modelmetadata_alert_model_version_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='confidence',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='is_correct',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]
