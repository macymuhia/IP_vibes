# Generated by Django 2.2.4 on 2019-09-07 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vibes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, default='/static/img/default.png', max_length=255, null=True, upload_to='vibes/'),
        ),
    ]
