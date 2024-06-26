from django.urls import path
from . import views


app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("", views.base, name="base"),
    path("<int:party_id>/", views.partyDetails, name="partyDetails"),
    path("profile/<int:user_id>/", views.userProfile, name="profile"),
    path('createParty/', views.createParty, name="createParty"),
    path('editParty/<int:party_id>', views.editParty, name="editParty"),
    path("<int:party_id>/recension/new/", views.new_recension, name="new_recension"),
    path("<int:party_id>/request/new/", views.new_request, name="new_request"),
    path('<int:party_id>/request/deny/', views.deny_request, name="deny_request"),
    path(
        "<int:req_id>/request/decision/",
        views.requestDecision,
        name="requestDecision",
    ),
]
