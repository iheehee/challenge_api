# Generated by Django 5.0 on 2024-03-12 02:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0010_alter_challenge_owner'),
        ('user', '0017_rename_my_challenges_profile_my_closed_challenges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
        migrations.AddField(
            model_name='user',
            name='nickname_id',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='user', to='user.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='my_closed_challenges',
            field=models.ManyToManyField(blank=True, default='', related_name='profile_my_closed_challenges', to='challenge.challenge'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(default='', max_length=20),
        ),
    ]
