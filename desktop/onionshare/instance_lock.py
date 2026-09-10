# -*- coding: utf-8 -*-
"""
OnionShare | https://onionshare.org/

Copyright (C) 2014-2026 Micah Lee, et al. <micah@micahflee.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os


def acquire_flatpak_lock(lock_filename):
    """Acquire the Flatpak GUI lock using an OS-managed advisory lock.

    Flatpak instances can reuse the same PID inside separate PID namespaces,
    so the PID stored in the lock file cannot determine whether the previous
    OnionShare process is still alive. ``flock`` is tied to the open file
    description instead: the kernel releases it automatically when a process
    exits or crashes.

    Returns ``(lock_file, None)`` when this process owns the lock, otherwise
    ``(None, existing_pid)`` when another process still owns it.
    """
    import fcntl

    lock_file = open(lock_filename, "a+")
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_file.seek(0)
        existing_pid = lock_file.read().strip() or "unknown"
        lock_file.close()
        return None, existing_pid

    lock_file.seek(0)
    lock_file.truncate()
    lock_file.write(f"{os.getpid()}\n")
    lock_file.flush()
    return lock_file, None
