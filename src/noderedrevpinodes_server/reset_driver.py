# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2020-2025 Sven Sager
# SPDX-License-Identifier: GPL-2.0-or-later
"""
Watchdog systems to monitor plc program and reset_driver of piCtory.

This is a copy of revpipyload project module "watchdogs"
https://github.com/naruxde/revpipyload/blob/b51c2b617a57cc7d96fd67e1da9f090a0624eacb/src/revpipyload/watchdogs.py
"""

import os
from fcntl import ioctl
from logging import getLogger
from threading import Thread

log = getLogger(__name__)

PROCESS_IMAGE = "/dev/piControl0"


class ResetDriverWatchdog(Thread):
    """Watchdog to catch a piCtory reset_driver action."""

    def __init__(self):
        super(ResetDriverWatchdog, self).__init__()
        self.daemon = True
        self._calls = []
        self._exit = False
        self._fh = None
        self.not_implemented = False
        """True, if KB_WAIT_FOR_EVENT is not implemented in piControl."""
        self._triggered = False
        self.start()

    def run(self):
        """
        Mainloop of watchdog for reset_driver.

        If the thread can not open the process image or the IOCTL is not
        implemented (wheezy), the thread function will stop. The trigger
        property will always return True.
        """
        log.debug("enter ResetDriverWatchdog.run()")

        try:
            self._fh = os.open(PROCESS_IMAGE, os.O_RDONLY)
        except Exception:
            self.not_implemented = True
            log.error(
                "can not open process image at '{0}' for piCtory reset_driver watchdog"
                "".format(PROCESS_IMAGE)
            )
            return

        # The ioctl will return 2 byte (c-type int)
        byte_buff = bytearray(2)
        while not self._exit:
            try:
                rc = ioctl(self._fh, 19250, byte_buff)
                if rc == 0 and byte_buff[0] == 1:
                    self._triggered = True
                    log.debug("piCtory reset_driver detected")
                    for func in self._calls:
                        func()
            except Exception:
                self.not_implemented = True
                os.close(self._fh)
                self._fh = None
                log.warning("IOCTL KB_WAIT_FOR_EVENT is not implemented")
                return

        log.debug("leave ResetDriverWatchdog.run()")

    def register_call(self, function):
        """Register a function, if watchdog triggers."""
        if not callable(function):
            return ValueError("Function is not callable.")
        if function not in self._calls:
            self._calls.append(function)

    def stop(self):
        """Stop watchdog for piCtory reset_driver."""
        log.debug("enter ResetDriverWatchdog.stop()")

        self._exit = True
        if self._fh is not None:
            os.close(self._fh)
            self._fh = None

        log.debug("leave ResetDriverWatchdog.stop()")

    def unregister_call(self, function=None):
        """Remove a function call on watchdog trigger."""
        if function is None:
            self._calls.clear()
        elif function in self._calls:
            self._calls.remove(function)

    @property
    def triggered(self):
        """Will return True one time after watchdog was triggered."""
        rc = self._triggered
        self._triggered = False
        return rc
