# Generated by Django 4.2.6 on 2023-12-28 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_alter_author_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
