# Generated by Django 5.0 on 2024-01-03 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0005_alter_challenge_certifications_photoexample'),
        ('user', '0009_alter_profile_my_certifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='my_certifications',
            field=models.ManyToManyField(blank=True, default='', related_name='profile_certifications', to='challenge.certification'),
        ),
    ]
