import django_filters
from apps.leads.models import Lead


class LeadFilter(django_filters.FilterSet):
    class Meta:
        model = Lead
        fields = [
            "status",
            "assigned_to",
            "created_by",
            "company",
        ]
