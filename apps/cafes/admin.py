from django.contrib import admin

from apps.cafes.models import Cafe


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    pass
