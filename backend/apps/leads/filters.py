# ==============================================================================
# Lead Query Filters
# ==============================================================================

import django_filters
from apps.leads.models import Lead


class LeadFilter(django_filters.FilterSet):
    """Provide supported query filters for lead listings."""

    class Meta:
        model = Lead
        fields = [
            "status",
            "assigned_to",
            "created_by",
            "company",
        ]
