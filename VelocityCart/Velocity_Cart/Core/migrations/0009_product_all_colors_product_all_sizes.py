# Generated by Django 4.2.7 on 2023-12-01 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0008_alter_ratings_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='all_colors',
            field=models.CharField(default='All colors are available.', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='all_sizes',
            field=models.CharField(default='All sizes are available.', max_length=50),
        ),
    ]
