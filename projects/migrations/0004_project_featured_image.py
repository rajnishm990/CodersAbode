# Generated by Django 4.0.6 on 2022-07-14 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_vote_ratio_alter_project_vote_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
