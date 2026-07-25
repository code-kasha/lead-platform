# ==============================================================================
# Note Model Tests
# ==============================================================================


from apps.leads.tests.factories import create_lead, create_note
from django.test import TestCase


class LeadNoteModelTests(TestCase):
    """Verify lead note model behaviour."""

    def test_create_note(self):
        note = create_note()

        self.assertEqual(
            note.content,
            "Test note",
        )

    def test_note_belongs_to_lead(self):
        lead = create_lead()

        note = create_note(
            lead=lead,
        )

        self.assertEqual(
            note.lead,
            lead,
        )

    def test_note_has_author(self):
        note = create_note()

        self.assertIsNotNone(
            note.author,
        )

    def test_note_string_representation(self):
        note = create_note()

        self.assertIn(
            "Note by",
            str(note),
        )

    def test_note_ordering(self):
        create_note(
            content="First",
        )

        newest = create_note(
            content="Second",
        )

        self.assertEqual(
            newest.__class__.objects.first(),
            newest,
        )
