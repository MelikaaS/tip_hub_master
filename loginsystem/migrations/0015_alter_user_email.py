# Generated by Django 4.1.1 on 2022-11-02 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginsystem', '0014_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=60, verbose_name='email address'),
        ),
    ]
