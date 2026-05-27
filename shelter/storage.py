from db_file_storage.storage import DatabaseFileStorage
from django.urls import reverse
from django.utils.http import urlencode


class InlineDatabaseFileStorage(DatabaseFileStorage):
    """Serve files inline (no Content-Disposition: attachment) so <img> tags render."""

    def url(self, name: str) -> str:
        return reverse("db_file_storage.get_file") + "?" + urlencode({"name": name})
