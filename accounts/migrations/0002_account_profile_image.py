# Generated by Django 4.2.2 on 2023-06-16 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(blank=True, default='default-avatar.png', null=True, upload_to='photos/users/'),
        ),
    ]
