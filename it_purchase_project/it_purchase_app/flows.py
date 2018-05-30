from viewflow import flow, frontend
from viewflow.base import Flow
from viewflow.lock import select_for_update_lock

from .models import PurchaseProcess, PurchaseTask
from . import view


@frontend.register
class PurchaseFlow(Flow):
    """

    Leave Workflow
    """
    process_class = PurchaseProcess
    task_class = PurchaseTask
    lock_impl = select_for_update_lock

    summary_template = """
        Purchase Form For Gozen Hold.
        """

    start = (
        flow.Start(view.StartView)
            .Permission('it_purchase_app.can_create_purchase')
            .Next("")
    )

    end = flow.End()
