# Generated by Django 5.0 on 2024-01-07 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_userprofile_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='class_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]