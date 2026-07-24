from apps.leads.choices import LeadStatus

ALLOWED_STATUS_TRANSITIONS: dict[
    LeadStatus,
    set[LeadStatus],
] = {
    LeadStatus.NEW: {
        LeadStatus.CONTACTED,
        LeadStatus.LOST,
    },
    LeadStatus.CONTACTED: {
        LeadStatus.QUALIFIED,
        LeadStatus.LOST,
    },
    LeadStatus.QUALIFIED: {
        LeadStatus.PROPOSAL,
        LeadStatus.LOST,
    },
    LeadStatus.PROPOSAL: {
        LeadStatus.WON,
        LeadStatus.LOST,
    },
    LeadStatus.WON: set(),
    LeadStatus.LOST: set(),
}
