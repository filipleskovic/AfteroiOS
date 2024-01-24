from django.shortcuts import render, get_object_or_404
from app.models import Party, PartyPosters

# Create your views here.


def index(request):
    context = {}
    return render(request, "app/index.html", context)


def partyDetails(request, party_id):
    party = get_object_or_404(Party, pk=party_id)
    context = {
        "party": party,
        "image": party.party_poster_fk.party_url,
    }
    return render(request, "app/partyDetails.html", context)
