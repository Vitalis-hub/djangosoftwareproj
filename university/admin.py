from django.contrib import admin
from .models import Campus, Location, Entrance


class CampusAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass


class EntranceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Campus, CampusAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Entrance, EntranceAdmin)
