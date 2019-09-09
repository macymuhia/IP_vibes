from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='vibes/',
                              max_length=255, null=True, blank=True, default='/static/img/default.png')
    phone = models.CharField(max_length=20, blank=True, default='')
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField()


# def create_profile(sender, **kwargs):
#     user = kwargs["instance"]
#     if kwargs["created"]:
#         user_profile = UserProfile(user=user, bio='my bio')
#         user_profile.save()


# post_save.connect(create_profile, sender=User)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class Project(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='projects/')
    description = models.CharField(max_length=255)
    link = models.URLField(default='')
    project_owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    design_rating = models.DecimalField(
        max_digits=3, decimal_places=1, default=0, blank=True)
    usability_rating = models.DecimalField(
        max_digits=3, decimal_places=1, default=0, blank=True)
    content_rating = models.DecimalField(
        max_digits=3, decimal_places=1, default=0, blank=True)

    @classmethod
    def fetch_project(cls, project_id):
        return cls.objects.filter(project_owner__id=project_id)
