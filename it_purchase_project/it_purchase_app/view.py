from django.views import generic
from material import Layout, Row
from viewflow.flow.views import StartFlowMixin, FlowMixin
from viewflow.decorators import flow_view
from .forms import PurchaseForm, SupportForm
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
        purchase = form.save()
        self.activation.process.purchase = purchase
        super(StartView, self).activation_done(form)


# class SupportView(FlowMixin, generic.UpdateView):
#
#     form_class = SupportForm
#     layout = Layout(
#         'support_comment',
#
#     )
#
#     def get_object(self):
#         return self.activation.process.purchase
#
#     def activation_done(self, form):
#         purchase = form.save(commit=False)
#         purchase.support_comment = form.cleaned_data['support_comment']
#         purchase.save()
#         self.activation.process.purchase = purchase
#         super(SupportView, self).activation_done(form)

@flow_view
def support_view(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    purchase_request = request.activation.process.purchase.description
    form = forms.SupportForm(data=request.POST or None, initial={
        "started": datetime.datetime.now(),

    },
                             instance=request.process.purchase)

    if request.method == "POST":

        if form.is_valid():
            purchase = form.save()
            request.activation.process.purchase = purchase
            request.activation.done()

            return redirect(
                get_next_task_url(request, request.activation.process))

    return render(request, 'it_purchase_app/support.html', {
        'form': form,
        'activation': request.activation,
        'created_by': request.task.get_previous_by_created().owner.username,
        'purchase_request': purchase_request,
    })


class PurchaseView(FlowMixin, generic.UpdateView):
    def get_object(self):
        return self.activation.process.purchase


@flow_view
def is_need_price_quote(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    purchase_request = request.activation.process.purchase.description
    support_comment = request.activation.process.purchase.support_comment
    form = forms.PriceQuoteForm(data=request.POST or None, initial={
        "started": datetime.datetime.now(),

    },
                                instance=request.process.purchase)

    if request.method == "POST":

        if form.is_valid():
            purchase = form.save()
            request.activation.process.purchase = purchase
            request.activation.done()

            return redirect(
                get_next_task_url(request, request.activation.process))

    return render(request, 'it_purchase_app/purchase_team.html', {
        'form': form,
        'activation': request.activation,
        'created_by': request.task.get_previous_by_created(

        ).get_previous_by_created().owner.username,
        'purchase_request': purchase_request,
        'support_comment': support_comment,
        'support_user': request.task.get_previous_by_created().owner.username,
    })
