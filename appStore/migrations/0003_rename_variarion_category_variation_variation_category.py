# Generated by Django 4.1.6 on 2023-05-23 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appStore', '0002_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='variarion_category',
            new_name='variation_category',
        ),
    ]
