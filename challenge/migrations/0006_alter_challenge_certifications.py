# Generated by Django 4.2.8 on 2023-12-20 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0005_alter_challenge_certifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='certifications',
            field=models.ManyToManyField(blank=True, related_name='Certifications', to='challenge.certification'),
        ),
    ]
