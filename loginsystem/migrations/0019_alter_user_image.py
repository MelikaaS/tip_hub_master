# Generated by Django 4.1.1 on 2022-12-21 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginsystem', '0018_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='codingwithmelika/default_image.png', null=True, upload_to='images/'),
        ),
    ]
