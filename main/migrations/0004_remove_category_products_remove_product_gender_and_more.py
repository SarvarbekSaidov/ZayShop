# Generated by Django 5.1.2 on 2024-10-31 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_category_options_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='products',
        ),
        migrations.RemoveField(
            model_name='product',
            name='gender',
        ),
        migrations.AddField(
            model_name='category',
            name='subtype',
            field=models.CharField(max_length=20, null='true', verbose_name='Category Subtype'),
            preserve_default='true',
        ),
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('Gender', 'Gender'), ('Sale', 'Sale'), ('Product', 'Product')], max_length=20, null='true', verbose_name='Category Type'),
            preserve_default='true',
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='products', to='main.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, null='true'),
        ),
    ]
