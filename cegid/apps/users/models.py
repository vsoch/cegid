from cegid.settings import STAFF_PICTURES
from django.contrib.auth.models import User
from django.db.models import Q, DO_NOTHING
from django.db import models
from jsonfield import JSONField
import os

class UserProfile(models.Model):

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    ROLE_CHOICES = (
        ("ADMIN", "ADMIN"), # all permissions
        ("STAFF", "STAFF"),
        ("FACULTY","FACULTY"),
        ("STUDENT","STUDENT")
    )
    def get_url(self):
        return os.path.basename(self.avatar.url)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField("user role",max_length=100,choices=ROLE_CHOICES,null=True,blank=True,help_text="Name of user role.")
    avatar = models.ImageField(upload_to="staff",max_length=500)
    description = models.CharField("staff description",max_length=1000,null=True,blank=True,help_text="Staff member description")
    name = models.CharField("staff full name",max_length=1000,null=True,blank=True,help_text="Staff member name")
    title = models.CharField("staff title",max_length=1000,null=True,blank=True,help_text="Staff member title or position")
