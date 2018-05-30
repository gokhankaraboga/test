from django.db import models
from django.contrib.auth.models import AbstractUser


JOB_TITLES = (('developer', 'Developer'), ('manager', 'Manager'))

class Profile(AbstractUser):
    job_title = models.CharField(choices=JOB_TITLES, blank=True,
                                 max_length=250)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'job_title']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        permissions = [
            ('can_approve_purchase', 'Can approve it_purchase_app form'),
            ('can_create_purchase', 'Can create it_purchase_app form'),

        ]
