# Generated by Django 5.1.2 on 2024-10-27 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_lesson_options_course_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='public_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
