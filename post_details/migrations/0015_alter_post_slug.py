# Generated by Django 4.1.1 on 2023-02-28 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_details', '0014_alter_teacher_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
