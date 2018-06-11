from .flows import PurchaseFlow
from viewflow.flow.viewset import FlowViewSet

urlpatterns = FlowViewSet(PurchaseFlow).urls
