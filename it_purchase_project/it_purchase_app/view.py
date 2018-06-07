from django.views import generic
from material import Layout, Row
from viewflow.flow.views import StartFlowMixin, FlowMixin

from .forms import PurchaseForm, SupportForm, NecessaryPriceQuoteForm, \
    GetPriceQuoteForm, ManagerApprovalForm


class CustomLayout(Layout):
    def __add__(self, x):
        elements = x.elements + self.elements
        return Layout(elements)


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


class PurchaseView(FlowMixin, generic.UpdateView):
    def get_object(self):
        return self.activation.process.purchase


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
    form_class = NecessaryPriceQuoteForm
    layout = CustomLayout(
        Row('description'),
        Row('created_by'),
        Row('support_comment'),
        Row('support_user'),
        Row('need_price_quote'),
        Row('purchase_team_comment'),
        Row('price_quoted'),

    )

    def get_object(self):
        return self.activation.process.purchase

    def activation_done(self, form):
        purchase = form.save(commit=False)
        self.activation.process.purchase = purchase
        purchase.purchase_user = self.request.user.username
        purchase.save()
        super(DoesNeedPriceQuote, self).activation_done(form)


class GetPriceQuote(FlowMixin, generic.UpdateView):
    layout = Layout(
        Row('description'),
        Row('created_by'),
        Row('support_comment'),
        Row('support_user'),
        Row('need_price_quote'),
        Row('purchase_team_comment'),
        Row('investigator_comment'),
        Row('price_quoted'),

    )
    form_class = GetPriceQuoteForm

    def get_object(self):
        return self.activation.process.purchase


class ManagerCheck(FlowMixin, generic.UpdateView):
    form_class = ManagerApprovalForm
    layout = Layout(
        Row('description'),
        Row('created_by'),
        Row('support_comment'),
        Row('support_user'),
        Row('need_price_quote'),
        Row('purchase_team_comment'),
        Row('investigator_comment'),
        Row('price_quoted'),
        Row('manager_comment'),
        Row('manager_approval'),
    )

    def get_object(self):
        return self.activation.process.purchase
