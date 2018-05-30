from django.db import models
from viewflow.models import Process, Task
from django.contrib.auth.models import AbstractUser


class Purchase(models.Model):
    User = 'profile.Profile'
    description = models.CharField(max_length=500, default="")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class PurchaseProcess(Process):
    purchase = models.ForeignKey("Purchase", blank=True, null=True,
                              on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Purchase process list'


class PurchaseTask(Task):
    class Meta:
        proxy = True

