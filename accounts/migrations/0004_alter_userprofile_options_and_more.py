# Generated by Django 4.2.2 on 2023-06-24 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'UserProfile', 'verbose_name_plural': 'UserProfiles'},
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_number',
        ),
    ]