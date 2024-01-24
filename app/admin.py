from django.contrib import admin

from app.models import Party, PartyGuest, PartyPosters, PartyRequest, Recension, User

admin.site.register(User)
admin.site.register(Party)
admin.site.register(PartyPosters)
admin.site.register(Recension)
admin.site.register(PartyGuest)
admin.site.register(PartyRequest)
