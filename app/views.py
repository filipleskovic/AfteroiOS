from asyncio.windows_events import NULL
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from app.models import Party, PartyPosters, PartyRequest
from django.urls import reverse
from . import forms


def base(request):
    user = request.user
    context = {
        "user": user,
    }
    return render(request, "app/base.html", context)


def index(request):
    context = {"parties": Party.objects.all()}
    return render(request, "app/index.html", context)


def partyDetails(request, party_id):
    party = get_object_or_404(Party, pk=party_id)
    user = request.user
    requests = PartyRequest.objects.filter(party_id=party_id)
    if user.is_authenticated:
        party_request = PartyRequest.objects.filter(
            user_id=user, party_id=party_id
        ).first()
    else:
        party_request = False
    context = {
        "party": party,
        "is_authenticated": user.is_authenticated,
        "party_request": party_request,
        "requests": requests,
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


def createParty(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = forms.PartyForm(request.POST)
        if form.is_valid():
            saved_party = form.save(commit=False)
            saved_party.created_by = request.user
            saved_party.save()
            return HttpResponseRedirect(reverse("app:index"))
    else:
        form = forms.PartyForm()
    posters = PartyPosters.objects.all()
    context = {
        "form": form,
        "action": "create",
        "posters": posters,
    }
    return render(request, "app/createParty.html", context)


def requestDecision(request, req_id):
    req = get_object_or_404(PartyRequest, pk=req_id)
    party_id = req.party_id.pk
    if request.method == "POST" and request.user.is_authenticated:
        inputvalue = request.POST.get("decision", None)
        if inputvalue == "Odobri":
            req.status = PartyRequest.APPROVED
        else:
            req.status = PartyRequest.DECLINED
        req.save()
    context = {}
    return HttpResponseRedirect(reverse("app:partyDetails", args=(party_id,)))
