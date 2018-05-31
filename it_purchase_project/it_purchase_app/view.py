from django.views import generic
from material import Layout, Row
from viewflow.flow.views import StartFlowMixin

from .forms import PurchaseForm


class StartView(StartFlowMixin, generic.UpdateView):
    form_class = PurchaseForm
    layout = Layout(
        Row('description'),
    )

    def get_object(self):
        return self.activation.process.purchase

    def activation_done(self, form):
        purchase = form.save()
        purchase.user = self.request.user
        purchase.save()
        self.activation.process.purchase = purchase
        super(StartView, self).activation_done(form)
