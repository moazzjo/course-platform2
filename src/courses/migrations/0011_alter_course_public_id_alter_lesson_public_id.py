# Generated by Django 5.1.2 on 2024-12-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_lesson_public_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='public_id',
            field=models.CharField(blank=True, db_index=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='public_id',
            field=models.CharField(blank=True, db_index=True, max_length=120, null=True),
        ),
    ]
