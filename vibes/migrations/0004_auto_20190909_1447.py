# Generated by Django 2.2.4 on 2019-09-09 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vibes', '0003_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
