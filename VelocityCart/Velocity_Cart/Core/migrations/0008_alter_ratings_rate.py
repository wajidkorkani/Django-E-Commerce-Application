# Generated by Django 4.2.7 on 2023-11-26 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0007_remove_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratings',
            name='rate',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True),
        ),
    ]
