from django.urls import path

from . import views


app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:party_id>/", views.partyDetails, name="partyDetails"),
    path("prrofile/<int:user_id>/",views.userProfile, name="profile")
]
