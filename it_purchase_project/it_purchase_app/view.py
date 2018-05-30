from django.views import generic
from material import Layout, Fieldset, Row, Span2, Span5, Span7

from viewflow.flow.views import StartFlowMixin, FlowMixin

from .forms import PurchaseForm


class StartView(StartFlowMixin, generic.UpdateView):
    form_class = PurchaseForm
    layout = Layout(
        Row('description'),
    )

    def get_object(self):
        return self.activation.process.leave

    def activation_done(self, form):
        leave = form.save()
        self.activation.process.leave = leave
        super(StartView, self).activation_done(form)
