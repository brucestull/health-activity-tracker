# Generated by Django 4.1.5 on 2023-02-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_is_moderator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_moderator',
            field=models.BooleanField(default=False, verbose_name='Is Moderator'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='registration_accepted',
            field=models.BooleanField(default=False, verbose_name='Registration Accepted'),
        ),
    ]
