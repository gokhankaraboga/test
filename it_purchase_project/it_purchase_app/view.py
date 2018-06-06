from django.views import generic
from material import Layout, Row
from viewflow.flow.views import StartFlowMixin, FlowMixin
from viewflow.decorators import flow_view
from .forms import PurchaseForm, SupportForm, PriceQuoteForm
from django.shortcuts import render, redirect
from viewflow.flow.views.utils import get_next_task_url
import datetime
from . import forms


class StartView(StartFlowMixin, generic.UpdateView):
    form_class = PurchaseForm
    layout = Layout(
        Row('description'),
    )

    def get_object(self):
        return self.activation.process.purchase

    def activation_done(self, form):
        purchase = form.save(commit=False)
        self.activation.process.purchase = purchase
        purchase.created_by = self.request.user.username
        purchase.save()
        super(StartView, self).activation_done(form)


# @flow_view
# def support_view(request, **kwargs):
#     request.activation.prepare(request.POST or None, user=request.user)
#     purchase_request = request.activation.process.purchase.description
#     form = forms.SupportForm(data=request.POST or None, initial={
#         "started": datetime.datetime.now(),
#
#     },
#                              instance=request.process.purchase)
#
#     if request.method == "POST":
#
#         if form.is_valid():
#             purchase = form.save()
#             request.activation.process.purchase = purchase
#             request.activation.done()
#
#             return redirect(
#                 get_next_task_url(request, request.activation.process))
#
#     return render(request, 'it_purchase_app/support.html', {
#         'form': form,
#         'activation': request.activation,
#         'created_by': request.task.get_previous_by_created().owner.username,
#         'purchase_request': purchase_request,
#     })


class PurchaseView(FlowMixin, generic.UpdateView):
    def get_object(self):
        return self.activation.process.purchase


# @flow_view
# def is_need_price_quote(request, **kwargs):
#     request.activation.prepare(request.POST or None, user=request.user)
#     purchase_request = request.activation.process.purchase.description
#     support_comment = request.activation.process.purchase.support_comment
#     form = forms.PriceQuoteForm(data=request.POST or None, initial={
#         "started": datetime.datetime.now(),
#
#     },
#                                 instance=request.process.purchase)
#
#     if request.method == "POST":
#
#         if form.is_valid():
#             purchase = form.save()
#             request.activation.process.purchase = purchase
#             request.activation.done()
#
#             return redirect(
#                 get_next_task_url(request, request.activation.process))
#
#     return render(request, 'it_purchase_app/purchase_team.html', {
#         'form': form,
#         'activation': request.activation,
#         'created_by': request.task.get_previous_by_created(
#
#         ).get_previous_by_created().owner.username,
#         'purchase_request': purchase_request,
#         'support_comment': support_comment,
#         'support_user': request.task.get_previous_by_created().owner.username,
#     })

class SupportView(FlowMixin, generic.UpdateView):
    form_class = SupportForm
    layout = Layout(
        Row('support_comment'),
        Row('description'),
        Row('created_by'),
    )

    def get_object(self):
        return self.activation.process.purchase

    def activation_done(self, form):
        purchase = form.save(commit=False)
        purchase.support_user = self.request.user.username
        self.activation.process.purchase = purchase
        purchase.save()
        super(SupportView, self).activation_done(form)


class DoesNeedPriceQuote(FlowMixin, generic.UpdateView):
    form_class = PriceQuoteForm
    layout = Layout(
        Row('support_comment'),
        Row('description'),
        Row('created_by'),
        Row('need_price_quote'),
        Row('purchase_team_comment'),
        Row('support_user'),
    )

    def get_object(self):
        return self.activation.process.purchase

    def activation_done(self, form):
        purchase = form.save(commit=False)
        self.activation.process.purchase = purchase
        purchase.purchase_user = self.request.user.username
        purchase.save()
        super(DoesNeedPriceQuote, self).activation_done(form)

        # description = models.CharField(max_length=500, default="")
        # support_comment = models.CharField(max_length=500, default="")
        # need_price_quote = models.NullBooleanField(choices=BOOLEAN_CHOICES,
        #                                            blank=False, null=False)
        # purchase_team_comment = models.CharField(max_length=500, default="",
        #                                          null=True)
        #
        # created_by = models.CharField(max_length=500, default="")
        #
        # support_user = models.CharField(max_length=500, default="")