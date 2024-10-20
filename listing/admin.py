from django.contrib import admin
from listing.models import Agent, Property

admin.site.register(Property)
admin.site.register(Agent)