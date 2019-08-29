# Generated by Django 2.2.4 on 2019-08-29 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0013_auto_20190829_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parents',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='categories.Category'),
        ),
    ]
