from viewflow import flow, frontend
from viewflow.base import Flow, this
from viewflow.lock import select_for_update_lock

from .models import PurchaseProcess, PurchaseTask, YES
from . import view
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from viewflow.flow.views import CancelProcessView


@frontend.register
class PurchaseFlow(Flow):
    obsolete = flow.Obsolete()
    process_class = PurchaseProcess
    task_class = PurchaseTask
    lock_impl = select_for_update_lock

    summary_template = """
        Purchase Form For Gozen Hold.
        """

    start = (
        flow.Start(view.StartView)
            .Permission('profile.can_create_purchase')
            .Next(this.support)
    )

    support = (
        flow.View(
            view.SupportView,
        )
            .Permission('profile.can_support_purchase')
            .Next(this.check_support_approve)
    )
    check_support_approve = (
        flow.If(
            cond=lambda act: act.process.purchase.support_approval == YES,
            task_title=_('Check Approval of Support'),
        )
            .Then(this.price_quote)
            .Else(this.end)
    )

    price_quote = (
        flow.View(
            view.DoesNeedPriceQuote,
            task_title=_('Purchase Team Approval For Price Quote'),
            task_description=_("Does Need Get a Price Quote"),
        )
            .Permission('profile.can_purchase_team')
            .Next(this.check_price_quote)
    )

    check_price_quote = (
        flow.If(
            cond=lambda act: act.process.purchase.need_price_quote == YES,
            task_title=_('Check Necessity of Price Quote'),
        )
            .Then(this.get_price_quote)
            .Else(this.is_superior_approval_required)
    )

    get_price_quote = (
        flow.View(
            view.GetPriceQuote,
            task_title=_('Get a Price Quote '),
            task_description=_("Get a Price Quote"),
        )
            .Permission('profile.can_purchase_team')
            .Next(this.is_superior_approval_required)
    )

    is_superior_approval_required = (
        flow.If(cond=lambda
            activation: activation.process.is_superior_approval_required)
            .Then(this.superior_approval)
            .Else(this.end)
    )

    superior_approval = (
        flow.View(
            view.SuperiorApprovalCheck,
            task_title=_('Manager Approve For Purchase'),
            task_description=_("Approvement is required"),
            task_result_summary=_(
                "Purchase was {{ "
                "process.purchase.superior_approval|yesno:'Approved,Rejected'  "
                "}} by {{process.created_by}}"))
            .Permission('profile.can_approve_purchase').
            Assign(lambda act: act.process.superior_assign())
            .Next(this.check_superior_approval)
    )

    check_superior_approval = (
        flow.If(
            cond=lambda act: act.process.purchase.superior_approval == YES,
            task_title=_('Check Approval of Manager'),
        )
            .Then(this.proceed_purchase)
            .Else(this.end)
    )

    proceed_purchase = (flow.View(
        view.ProceedPurchase,
        task_title=_('Proceed Purchase'),
        task_description=_('Proceed Purchase'),
    ).Permission('profile.can_purchase_team').Next(
        this.end)
    )

    end = flow.End()

    # @method_decorator(
    #     flow.flow_func)
    # def perform_my_task(self, activation, **kwargs):
    #     activation.prepare()
    #     activation.cancel()
    #     activation.process.status
    #     activation.done()
    #     activation.gokhan
    #     a = adad


    #
    # def my_handler(self, activation):
    #     CancelProcessView.as_view()




