from viewflow import flow, frontend
from viewflow.base import Flow, this
from viewflow.lock import select_for_update_lock

from .models import PurchaseProcess, PurchaseTask
from . import view
from django.utils.translation import gettext as _


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
            view.support_view,
        )
            .Permission('profile.can_support_purchase')
            .Next(this.price_quote)
    )

    price_quote = (
        flow.View(
            view.is_need_price_quote,
            task_title=_('Purchase Team Approval For Price Quote'),
            task_description=_("Does Need Get a Price Quote"),
        )
            .Permission('profile.can_purchase_team')
            .Next(this.check_price_quote)
    )

    check_price_quote = (
        flow.If(
            cond=lambda act: act.process.purchase.need_price_quote,
            task_title=_('Check Necessity of Price Quote'),
        )
            .Then(this.get_price_quote)
            .Else(this.manager_check)
    )

    get_price_quote = (
        flow.View(
            view.PurchaseView, fields=['purchase_team_comment'],
            task_title=_('Get a Price Quote '),
            task_description=_("Get a Price Quote"),
        )
            .Permission('profile.can_purchase_team')
            .Next(this.manager_check)
    )

    manager_check = (
        flow.View(
            view.PurchaseView, fields=['manager_approved', 'manager_comment'],
            task_title=_('Manager Approve For Purchase'),
            task_description=_("Approvement is required"),
            task_result_summary=_(
                "Purchase was {{ process.approved|yesno:'Approved,Rejected' "
                "}}"))
            .Permission('profile.can_approve_purchase')
            .Next(this.end)
    )

    end = flow.End()
