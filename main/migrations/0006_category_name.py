# Generated by Django 5.1.2 on 2024-10-31 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
