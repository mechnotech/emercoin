# Generated by Django 3.1.7 on 2021-04-13 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0032_terms_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Privacy',
        ),
        migrations.DeleteModel(
            name='Terms',
        ),
    ]