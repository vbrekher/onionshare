from types import SimpleNamespace

from onionshare.tab.mode import file_selection


class FakeDragEvent:
    def __init__(self):
        self.ignored = False

    def ignore(self):
        self.ignored = True


def test_flatpak_drag_is_rejected_before_warning(monkeypatch):
    """Reject the active drag before opening the modal Flatpak warning."""
    event = FakeDragEvent()
    common = SimpleNamespace(is_flatpak=lambda: True)
    file_list = SimpleNamespace(common=common)

    monkeypatch.setattr(file_selection.strings, "_", lambda key: key)

    def assert_rejected_before_alert(common, message):
        assert event.ignored
        assert message == "gui_dragdrop_sandbox_flatpak"

    monkeypatch.setattr(file_selection, "Alert", assert_rejected_before_alert)

    file_selection.FileList.dragEnterEvent(file_list, event)

    assert event.ignored
