# -*- coding: utf-8 -*-
from builtins import _

import re

from pyload.plugins.internal.Addon import Addon


class LinkdecrypterComHook(Addon):
    __name__ = "LinkdecrypterComHook"
    __type__ = "hook"
    __version__ = "1.11"
    __status__ = "broken"

    __config__ = [("activated", "bool", "Activated", False),
                  ("pluginmode", "all;listed;unlisted", "Use for plugins", "all"),
                  ("pluginlist", "str", "Plugin list (comma separated)", ""),
                  ("reload", "bool", "Reload plugin list", True),
                  ("reloadinterval", "int", "Reload interval in hours", 12)]

    __description__ = """Linkdecrypter.com addon plugin"""
    __license__ = "GPLv3"
    __authors__ = [("Walter Purcaro", "vuolter@gmail.com")]

    def get_hosters(self):
        list = re.search(r'>Supported\(\d+\)</b>: <i>(.[\w\-., ]+)', self.load(
            "http://linkdecrypter.com/").replace("(g)", "")).group(1).split(', ')
        try:
            list.remove("download.serienjunkies.org")
        except ValueError:
            pass

        return list
