# Generated by Django 5.0 on 2024-03-11 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0010_alter_challenge_owner'),
        ('user', '0015_remove_profile_my_challenges_profile_my_challenges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='my_challenges',
            field=models.ManyToManyField(blank=True, default='', to='challenge.challenge'),
        ),
    ]
