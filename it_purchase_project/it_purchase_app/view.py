from django.views import generic
from material import Layout, Row, Fieldset
from viewflow.flow.views import StartFlowMixin, FlowMixin
from django import forms
from viewflow.nodes.view import Start
from .models import PurchaseProcess, PurchaseTask
from viewflow.flow.views import CancelProcessView

from .forms import PurchaseForm, SupportForm, NecessaryPriceQuoteForm, \
    GetPriceQuoteForm, SuperiorApprovalForm, ProceedPurchaseForm


class CustomLayout(Layout):
    def __add__(self, x):
        elements = x.elements + self.elements
        return CustomLayout(*elements)


class StartView(StartFlowMixin, generic.UpdateView):
    form_class = PurchaseForm
    layout = CustomLayout(
        Fieldset("Purchase Request",
                 'description'),
    )

    def get_object(self):
        return self.activation.process.purchase

    def activation_done(self, form):
        purchase = form.save(commit=False)
        self.activation.process.purchase = purchase
        # purchase.created_by = self.request.user.username
        purchase.save()
        super(StartView, self).activation_done(form)


class PurchaseView(FlowMixin, generic.UpdateView):
    def get_object(self):
        return self.activation.process.purchase


class SupportView(FlowMixin, generic.UpdateView):
    form_class = SupportForm
    layout = CustomLayout(
        Fieldset("Purchase Details",
        Row('created_by'),
        Row('description'),
    ),
        Fieldset("Support",
                 Row('support_comment'),
                 Row('support_approval'),
                 ))

    def get_form_kwargs(self):
        kwargs = super(SupportView, self).get_form_kwargs()
        task_dict = self.activation.process.get_task_map()

        kwargs['initial'].update(
            {
                "created_by":
                    task_dict['start'].owner.username})
        return kwargs

    def get_object(self):
        return self.activation.process.purchase

    def activation_done(self, form):
        purchase = form.save(commit=False)
        self.activation.process.purchase = purchase
        purchase.save()
        super(SupportView, self).activation_done(form)


class DoesNeedPriceQuote(FlowMixin, generic.UpdateView):
    form_class = NecessaryPriceQuoteForm
    layout = CustomLayout(
        Row('support_user'),
        Fieldset("Purchase Team",
                 Row('need_price_quote'),
                 Row('purchase_team_comment'),
                 Row('price_quoted','currency_quoted'), ),

    ) + SupportView.layout

    def get_form_kwargs(self):
        kwargs = super(DoesNeedPriceQuote, self).get_form_kwargs()
        task_dict = self.activation.process.get_task_map()
        kwargs['initial'].update(
            {
                "created_by":
                    task_dict['start'].owner.username,
                "support_user":
                    task_dict['support'].owner.username})
        return kwargs

    def get_object(self):
        return self.activation.process.purchase

    def activation_done(self, form):
        purchase = form.save(commit=False)
        self.activation.process.purchase = purchase
        purchase.save()
        super(DoesNeedPriceQuote, self).activation_done(form)


class GetPriceQuote(FlowMixin, generic.UpdateView):
    layout = CustomLayout(
        Row('support_user'),
        Fieldset("Purchase Team",
        Row('need_price_quote'),
        Row('purchase_team_comment'),
        Row('purchase_team_user'),
        Row('need_price_quote'),
        Row('investigator_comment'),
        Row('price_quoted','currency_quoted'),)

    ) + SupportView.layout
    form_class = GetPriceQuoteForm

    def get_object(self):
        return self.activation.process.purchase

    def get_form_kwargs(self):
        kwargs = super(GetPriceQuote, self).get_form_kwargs()
        task_dict = self.activation.process.get_task_map()

        kwargs['initial'].update(
            {
                "created_by":
                    task_dict['start'].owner.username,
                "support_user":
                    task_dict['support'].owner.username,
                "purchase_team_user": task_dict["price_quote"].owner.username
            })
        return kwargs


class SuperiorApprovalCheck(FlowMixin, generic.UpdateView):
    form_class = SuperiorApprovalForm
    layout = CustomLayout(
        Row('purchase_investigator_user'),
        Fieldset("Superior Comment",
        Row('superior_comment'),
        Row('superior_approval'),)
    ) + GetPriceQuote.layout

    def get_object(self):
        return self.activation.process.purchase

    def get_form_kwargs(self):
        kwargs = super(SuperiorApprovalCheck, self).get_form_kwargs()
        task_dict = self.activation.process.get_task_map()

        if kwargs["instance"].investigator_comment == "":
            self.layout = disable_purchase_comment_and_user(
                self.layout.elements)

        kwargs['initial'].update(
            {
                "created_by":
                    task_dict['start'].owner.username,
                "support_user":
                    task_dict['support'].owner.username,
                "purchase_team_user": task_dict["price_quote"].owner.username,
            })
        if self.activation.process.purchase.need_price_quote == 'Yes':
            kwargs["initial"].update(
                {"purchase_investigator_user": task_dict[
                    "get_price_quote"].owner.username})

        return kwargs


class ProceedPurchase(FlowMixin, generic.UpdateView):
    form_class = ProceedPurchaseForm

    layout = CustomLayout(
        Row('superior_user'),
        Fieldset("Proceed Purchase",
                 Row('purchase_confirmation_comment'),),
    ) + SuperiorApprovalCheck.layout

    def get_form_kwargs(self):
        kwargs = super(ProceedPurchase, self).get_form_kwargs()
        task_dict = self.activation.process.get_task_map()

        if kwargs["instance"].investigator_comment == "":
            self.layout = disable_purchase_comment_and_user(
                self.layout.elements)

        kwargs['initial'].update(
            {
                "created_by":
                    task_dict['start'].owner.username,
                "support_user":
                    task_dict['support'].owner.username,
                "purchase_team_user": task_dict["price_quote"].owner.username,
                "superior_user": task_dict["superior_approval"].owner.username,
            })
        if self.activation.process.purchase.need_price_quote == 'Yes':
            kwargs["initial"].update(
                {"purchase_investigator_user": task_dict[
                    "get_price_quote"].owner.username})

        return kwargs

    def get_object(self):
        return self.activation.process.purchase


def disable_purchase_comment_and_user(elements):
    temp_layout_elements = []
    for elm in elements:
        if elm.elements[0].field_name not in \
                ["investigator_comment", "purchase_investigator_user"]:
            temp_layout_elements.append(elm)
    return CustomLayout(*temp_layout_elements)
