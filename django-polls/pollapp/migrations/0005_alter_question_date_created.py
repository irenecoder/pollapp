# Generated by Django 4.0 on 2021-12-13 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollapp', '0004_alter_choice_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date_created',
            field=models.DateTimeField(),
        ),
    ]
