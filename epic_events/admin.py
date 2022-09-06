from django.contrib import admin

from epic_events.models import User, Customer, Event, Contract

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Event)
admin.site.register(Contract)
