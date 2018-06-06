from django.db import models
from viewflow.models import Process, Task
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

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
    purchase_team_comment = models.CharField(max_length=500, default="", null=True)
    manager_comment = models.CharField(max_length=500, default="")
    manager_approved = models.NullBooleanField(choices=BOOLEAN_CHOICES,
                                               blank=True, null=True)
    created_by = models.CharField(max_length=500, default="")

    support_user = models.CharField(max_length=500, default="")
    purchase_user = models.CharField(max_length=500, default="")

class PurchaseProcess(Process):
    purchase = models.ForeignKey("Purchase", blank=True, null=True,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Purchase process list'


class PurchaseTask(Task):
    class Meta:
        proxy = True

#
# class Support(models.Model):
#     comment = models.CharField(max_length=500, default="")
