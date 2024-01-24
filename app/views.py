from django.shortcuts import render, get_object_or_404
from app.models import Party, PartyPosters


def base(request):
    user = request.user
    context = {'user': user}
    return render(request, 'app/base.html', context)

def index(request):
    context = {"parties": Party.objects.all()}
    return render(request, "app/index.html", context)


def partyDetails(request, party_id):
    party = get_object_or_404(Party, pk=party_id)
    context = {
        "party": party,
        "image": party.party_poster_fk.party_url,
    }
    return render(request, "app/partyDetails.html", context)


def userProfile(request, user_id):
    context = {}
    return render(request, "app/profile.html", context)
