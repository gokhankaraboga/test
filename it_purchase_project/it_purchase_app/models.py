from django.db import models
from viewflow.models import Process, Task
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _
from .constants import *
from ..profile.models import Profile

BOOLEAN_CHOICES = (
    (None, 'Not Decided'),
    (True, 'Yes'),
    (False, 'No')
)


class Purchase(models.Model):
    description = models.CharField(max_length=500, default="")
    support_comment = models.CharField(max_length=500, default="")
    need_price_quote = models.NullBooleanField(choices=BOOLEAN_CHOICES,
                                               blank=False, null=False)
    purchase_team_comment = models.CharField(max_length=500, default="",
                                             null=True)
    manager_comment = models.CharField(max_length=500, default="")
    manager_approval = models.NullBooleanField(choices=BOOLEAN_CHOICES,
                                               blank=True, null=True)
    created_by = models.CharField(max_length=500, default="")

    support_user = models.CharField(max_length=500, default="")
    purchase_user = models.CharField(max_length=500, default="")
    purchase_team_investigator = models.CharField(max_length=500, default="")
    investigator_comment = models.CharField(max_length=500, default="")
    price_quoted = models.FloatField(default=0.0)


class PurchaseProcess(Process):
    purchase = models.ForeignKey("Purchase", blank=True, null=True,
                                 on_delete=models.CASCADE)

    @property
    def is_manager_approval_required(self):
        # TODO DJANGO ORM QUERY OPTIMIZATION
        groups = Profile.objects.get(
            username=self.purchase.created_by).groups.all()
        max_limit = 0

        for group in groups:
            if group.name in PERMISSION_ALWAYS_GRANTED_GROUPS:
                return False
            if PERSONAL_LIMITS[group.name] > max_limit:
                max_limit = PERSONAL_LIMITS.get(group.name, 0)

        if self.purchase.price_quoted > max_limit:
            return True

        return False

    class Meta:
        verbose_name_plural = 'Purchase process list'


class PurchaseTask(Task):
    class Meta:
        proxy = True

#
# class Support(models.Model):
#     comment = models.CharField(max_length=500, default="")
