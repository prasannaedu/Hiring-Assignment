from django.urls import path
from app.api.viewsets.interaction import (
    RecentInteractionsView,
    TopContactsView,
    SpamReportsView,
    CreateInteractionView,  # ✅ added
)

urlpatterns = [
    path('interactions/', CreateInteractionView.as_view(), name='create-interaction'),  # ✅ added
    path('interactions/recent', RecentInteractionsView.as_view(), name='recent-interactions'),
    path('interactions/top', TopContactsView.as_view(), name='top-contacts'),
    path('interactions/spam-reports', SpamReportsView.as_view(), name='spam-reports'),
]
