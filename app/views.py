from asyncio.windows_events import NULL
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from app.models import Party, PartyPosters, PartyRequest, Recension, PartyGuest, User
from django.urls import reverse
from django.db.models import Count, Avg
from . import forms


def base(request):
    user = request.user
    context = {
        "user": user,
    }
    return render(request, "app/base.html", context)


def index(request):
    context = {"parties": Party.objects.all(),
               "user": request.user}
    return render(request, "app/index.html", context)


def partyDetails(request, party_id):
    party = get_object_or_404(Party, pk=party_id)
    user = request.user
    requests = PartyRequest.objects.filter(party_id=party_id)
    if user.is_authenticated:
        party_request = PartyRequest.objects.filter(
            user_id=user, party_id=party_id
        ).first()
        guest = PartyGuest.objects.filter(party_id=party, user_id=user).first()
    else:
        party_request = False
        guest = None
    if not party.is_finished():
        recensions = None
    else:
        recensions = Recension.objects.filter(party_id=party)
    context = {
        "party": party,
        "party_request": party_request,
        "requests": requests,
        "recensions": recensions,
        "numberOfPending":PartyRequest.objects.filter(party_id=party, status="PENDING"),
        "guest": guest,
    }
    return render(request, "app/partyDetails.html", context)


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


def new_recension(request, party_id):
    party = get_object_or_404(Party, pk=party_id)
    if request.method == "POST" and request.user.is_authenticated:
        text = request.POST["text"]
        ocjena = request.POST["ocjena"]
        partyRecension = Recension(
            party_id=party,
            user_id=request.user,
            text=text,
            rating=ocjena
        )
        partyRecension.save()
    return HttpResponseRedirect(reverse("app:partyDetails", args=(party_id,)))

def deny_request(request, party_id):
    party = get_object_or_404(Party, pk=party_id)
    user = request.user
    requests = PartyRequest.objects.filter(party_id=party)
    guests = PartyGuest.objects.filter(party_id=party)
    if request.method == "POST" and request.user.is_authenticated:
        guests.filter(user_id=user).delete()
        requests.filter(user_id=user).delete()
    return HttpResponseRedirect(reverse("app:partyDetails", args=(party_id,)))
    


def userProfile(request, user_id):
    user_data = get_object_or_404(User, pk=user_id)
    parties = Party.objects.filter(created_by=user_id)
    total_parties = parties.count()
    user_recensions = Recension.objects.filter(party_id__in=parties)
    average_rating = user_recensions.aggregate(Avg("rating"))["rating__avg"]

    previous_parties = user_data.get_previous_parties()
    current_parties = user_data.get_current_parties()
    attended_parties = user_data.get_attended_parties()

    previous_parties_dto = []

    for party in previous_parties:
        previous_parties_dto.append(
            {
                "party_details": party,
                "recensions": Recension.objects.filter(party_id=party.id),
            }
        )

    current_parties_dto = []

    for party in current_parties:
        current_parties_dto.append(
            {
                "party_details": party,
                "recensions": Recension.objects.filter(party_id=party.id),
            }
        )

    attended_parties_dto = []

    for party in attended_parties:
        attended_parties_dto.append(
            {
                "party_details": party,
                "recensions": Recension.objects.filter(party_id=party.id),
            }
        )

    context = {
        "user_data": user_data,
        "parties": parties,
        "total_parties": total_parties,
        "average_rating": average_rating,
        "previous_parties": previous_parties_dto,
        "current_parties": current_parties_dto,
        "attended_parties": attended_parties_dto,
    }
    return render(request, "app/profile.html", context)


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
        "posters": posters,
    }
    return render(request, "app/createParty.html", context)


def requestDecision(request, req_id):
    req = get_object_or_404(PartyRequest, pk=req_id)
    party_id = req.party_id.pk
    if request.method == "POST" and request.user.is_authenticated:
        inputvalue = request.POST.get("decision", None)
        if inputvalue == "Approve":
            req.status = PartyRequest.APPROVED
            guest = PartyGuest(party_id=req.party_id, user_id=req.user_id)
            guest.save()
        else:
            req.status = PartyRequest.DECLINED
        req.save()
    return HttpResponseRedirect(reverse("app:partyDetails", args=(party_id,)))



def editParty(request, party_id):
    party= get_object_or_404(Party, id=party_id)
    posters = PartyPosters.objects.all()
    if request.user.is_authenticated and request.method == "GET":
        form = forms.PartyForm(instance=party)
        context = {
        "form": form,
        "posters": posters,
    }
        return render(request, "app/createParty.html", context)
    if request.user.is_authenticated and request.method == "POST":
        form = forms.PartyForm(request.POST)
        if form.is_valid():
            party.title = form.cleaned_data['title']
            party.total_allowed_guest = form.cleaned_data['total_allowed_guest']
            party.description = form.cleaned_data['description']
            party.starts_at = form.cleaned_data['starts_at']
            party.closed_at = form.cleaned_data['closed_at']
            party.location = form.cleaned_data['location']
            party.party_poster_fk = form.cleaned_data['party_poster_fk']
            party.save()
            return HttpResponseRedirect(reverse("app:partyDetails", args=(party_id,)))
    return render(request, "app/partyDetails.html")
