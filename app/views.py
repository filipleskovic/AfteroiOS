from asyncio.windows_events import NULL
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from app.models import Party, PartyPosters, PartyRequest
from django.urls import reverse


def base(request):
    user = request.user
    context = {"user": user}
    return render(request, "app/base.html", context)


def index(request):
    context = {"parties": Party.objects.all()}
    return render(request, "app/index.html", context)


def partyDetails(request, party_id):
    party = get_object_or_404(Party, pk=party_id)
    user = request.user
    if user.is_authenticated:
        party_request = PartyRequest.objects.filter(user_id = user, party_id = party_id).first()
    
    context = {
        "party": party,
        "is_authenticated": user.is_authenticated,
        "party_request": party_request
    }
    return render(request, "app/partyDetails.html", context)


def userProfile(request, user_id):
    context = {}
    return render(request, "app/profile.html", context)


def new_request(request, party_id):
    party = get_object_or_404(Party, pk=party_id)
    if request.method == "POST" and request.user.is_authenticated:
        text = request.POST["text"]
        partyReq = PartyRequest(
            party_id=party,
            user_id=request.user,
            status=PartyRequest.PENDING,
            text=text,
        )
        partyReq.save()
    return HttpResponseRedirect(reverse("app:partyDetails", args=(party_id,)))
