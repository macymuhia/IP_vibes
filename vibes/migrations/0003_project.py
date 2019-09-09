# Generated by Django 2.2.4 on 2019-09-09 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vibes', '0002_auto_20190908_0026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='projects/')),
                ('description', models.CharField(max_length=255)),
                ('link', models.URLField(default='')),
                ('design_rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('usability_rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('content_rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('project_owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vibes.UserProfile')),
            ],
        ),
    ]
