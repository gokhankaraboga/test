from django.contrib.auth.models import AbstractUser
from django.db import models
from viewflow.models import Process, Task

from .constants import *
from ..profile.models import Profile

BOOLEAN_CHOICES = (
    ('None', 'Not Decided'),
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
    superior_comment = models.CharField(max_length=500, default="")
    superior_approval = models.CharField(choices=BOOLEAN_CHOICES,
                                         blank=True, null=True, max_length=500)
    investigator_comment = models.CharField(max_length=500, default="")
    price_quoted = models.FloatField(blank=True, null=True)
    support_approval = models.CharField(choices=BOOLEAN_CHOICES,
                                        blank=True, null=True, max_length=500)


class PurchaseTask(Task):
    class Meta:
        proxy = True

    def get_previous_process_created_by(self, previous_step):
        obj = PurchaseTask.objects.get(pk=self.pk - previous_step).owner

        if not obj:
            print("adsad")
        return obj


class PurchaseProcess(Process):
    purchase = models.ForeignKey("Purchase", blank=True, null=True,
                                 on_delete=models.CASCADE)

    @property
    def is_superior_approval_required(self):
        # TODO DJANGO ORM QUERY OPTIMIZATION
        groups = Profile.objects.get(
            username=self.get_task_map()["start"].owner.username).groups.all()
        max_limit = 0

        for group in groups:
            if group.name in PERMISSION_ALWAYS_GRANTED_GROUPS:
                return False
            if PERSONAL_LIMITS[group.name] > max_limit:
                max_limit = PERSONAL_LIMITS.get(group.name, 0)

        if not self.purchase.price_quoted:
            raise Exception(
                "Price quote must be specified in previous steps"
            )
        if self.purchase.price_quoted > max_limit:
            return True

        return False

    def superior_assign(self):
        groups = Profile.objects.get(
            username=self.get_task_map()["start"].owner.username).groups.all()

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

    # def get_previous_process_created_by(self, previous_step):
    #     return PurchaseTask.objects.get(pk=self.pk - previous_step)

    def get_task_map(self):
        task_dict = {}
        for task in list(self.task_set.all()):
            task_dict[task.flow_task.name] = task

        return task_dict

    class Meta:
        verbose_name_plural = 'Purchase process list'

# class PurchaseTask(Task):
#     class Meta:
#         proxy = True

#
# class Support(models.Model):
#     comment = models.CharField(max_length=500, default="")
