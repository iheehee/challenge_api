# Generated by Django 5.0 on 2024-05-16 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0017_alter_certificationdetail_certification_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='certification_comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='certification',
            name='certification_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='certification',
            name='certification_local_photo_url',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='certification',
            name='certification_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='certification',
            name='certification_photo',
            field=models.FileField(blank=True, default='', null=True, upload_to='certification'),
        ),
        migrations.DeleteModel(
            name='CertificationDetail',
        ),
    ]
