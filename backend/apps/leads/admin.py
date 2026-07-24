# ==============================================================================
# Admin configuration for the leads app
# ==============================================================================

from django.contrib import admin

from .models import Lead, LeadActivity, LeadNote


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "last_name",
        "email",
        "status",
        "assigned_to",
        "created_at",
    )

    list_filter = (
        "status",
        "assigned_to",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "company",
    )


@admin.register(LeadNote)
class LeadNoteAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "author",
        "created_at",
    )


@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "activity_type",
        "user",
        "created_at",
    )
