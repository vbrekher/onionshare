import os

from onionshare.instance_lock import acquire_flatpak_lock


def test_flatpak_lock_reclaims_stale_reused_pid(tmp_path):
    """A leftover PID must not block a new Flatpak process after a crash."""
    lock_filename = tmp_path / "lock"
    lock_filename.write_text(f"{os.getpid()}\n")

    lock_file, existing_pid = acquire_flatpak_lock(str(lock_filename))
    try:
        assert lock_file is not None
        assert existing_pid is None
        assert lock_filename.read_text() == f"{os.getpid()}\n"
    finally:
        lock_file.close()


def test_flatpak_lock_blocks_live_instance_and_recovers_after_release(tmp_path):
    """The advisory lock distinguishes a live process from stale PID text."""
    lock_filename = tmp_path / "lock"

    first_lock, existing_pid = acquire_flatpak_lock(str(lock_filename))
    assert first_lock is not None
    assert existing_pid is None

    second_lock, existing_pid = acquire_flatpak_lock(str(lock_filename))
    assert second_lock is None
    assert existing_pid == str(os.getpid())

    first_lock.close()

    recovered_lock, existing_pid = acquire_flatpak_lock(str(lock_filename))
    try:
        assert recovered_lock is not None
        assert existing_pid is None
    finally:
        recovered_lock.close()
