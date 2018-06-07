from django.db import models
from viewflow.models import Process, Task
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _
from .constants import *
from ..profile.models import Profile

BOOLEAN_CHOICES = (
    ('Not Decided', 'Not Decided'),
    ('Yes', 'Yes'),
    ('No', 'No')
)


class Purchase(models.Model):
    description = models.CharField(max_length=500, default="")
    support_comment = models.CharField(max_length=500, default="")
    need_price_quote = models.CharField(choices=BOOLEAN_CHOICES,
                                        blank=False, null=False, max_length=500)
    purchase_team_comment = models.CharField(max_length=500, default="",
                                             null=True)
    manager_comment = models.CharField(max_length=500, default="")
    manager_approval = models.CharField(choices=BOOLEAN_CHOICES,
                                        blank=True, null=True, max_length=500)
    created_by = models.CharField(max_length=500, default="")

    support_user = models.CharField(max_length=500, default="")
    purchase_user = models.CharField(max_length=500, default="")
    purchase_team_investigator = models.CharField(max_length=500, default="")
    investigator_comment = models.CharField(max_length=500, default="")
    price_quoted = models.FloatField(blank=True, null=True)


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

    @property
    def assign(self):
        groups = Profile.objects.get(
            username=self.purchase.created_by).groups.all()

        max_rank = TITLES_WEIGHT[DEVELOPER_TITLE] + 1
        for group in groups:
            if TITLES_WEIGHT.get(group.name):
                if TITLES_WEIGHT[group.name] < max_rank:
                    max_rank = TITLES_WEIGHT[group.name]
        if max_rank == TITLES_WEIGHT[DEVELOPER_TITLE] + 1:
            raise Exception(
                "User doesn't have any proper group for purchase app")

        superior_title = None

        for k, v in TITLES_WEIGHT.items():
            if v == max_rank - 1:
                superior_title = k
                break

        return Profile.objects.filter(groups__name=superior_title).first()

    class Meta:
        verbose_name_plural = 'Purchase process list'


class PurchaseTask(Task):
    class Meta:
        proxy = True

#
# class Support(models.Model):
#     comment = models.CharField(max_length=500, default="")
