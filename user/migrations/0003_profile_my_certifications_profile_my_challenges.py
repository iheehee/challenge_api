# Generated by Django 4.2.8 on 2023-12-14 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0003_challengeapply_certification'),
        ('user', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='my_certifications',
            field=models.ManyToManyField(related_name='profile_certifications', through='challenge.Certification', to='challenge.challenge'),
        ),
        migrations.AddField(
            model_name='profile',
            name='my_challenges',
            field=models.ManyToManyField(through='challenge.ChallengeApply', to='challenge.challenge'),
        ),
    ]