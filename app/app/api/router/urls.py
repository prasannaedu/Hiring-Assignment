from django.urls import path
from app.api.viewsets.user import CreateUser, LoginUser
from app.api.viewsets.interaction import (
    CreateInteractionView,
    RecentInteractionsView,
    TopContactsView,
    SpamReportsView
)
from app.api.viewsets.contact import CreateContact
from app.api.viewsets.search import SearchView, SearchDetailView

urlpatterns = [
    # User
    path('user/signup', CreateUser.as_view(), name='signup'),
    path('user/login', LoginUser.as_view(), name='login'),

    # Interaction
    path('interactions/', CreateInteractionView.as_view(), name='create-interaction'),
    path('interactions/recent', RecentInteractionsView.as_view(), name='recent-interactions'),
    path('interactions/top', TopContactsView.as_view(), name='top-contacts'),
    path('interactions/spam-reports', SpamReportsView.as_view(), name='spam-reports'),

    # Contact
    path('contact/', CreateContact.as_view(), name='create-contact'),

    # Search
    path('search/', SearchView.as_view(), name='search'),
    path('search/detail/<uuid:id>', SearchDetailView.as_view(), name='search-detail'),
]
