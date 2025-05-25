from django.urls import path
from .views import *

urlpatterns = [
    path('apply/', ApplyAgentView.as_view(), name='apply-agent'),
    path('status/', AgentStatusView.as_view(), name='agent-status'),
    path('applications/', AdminAgentApplicationsView.as_view(), name='admin-agent-apps'),
    path('applications/<int:pk>/approve/', ApproveAgentApplicationView.as_view(), name='approve-agent'),
    path('applications/<int:pk>/reject/', RejectAgentApplicationView.as_view(), name='reject-agent'),
    path('agencies/', AgencyListView.as_view(), name='agency-list'),
    path('advantages/', AdvantageListView.as_view(), name='advantage-list'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
]
