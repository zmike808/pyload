# -*- coding: utf-8 -*-
from builtins import _

from pyload.plugins.internal.XFSAccount import XFSAccount


class EasybytezCom(XFSAccount):
    __name__ = "EasybytezCom"
    __type__ = "account"
    __version__ = "0.18"
    __status__ = "testing"

    __description__ = """EasyBytez.com account plugin"""
    __license__ = "GPLv3"
    __authors__ = [("zoidberg", "zoidberg@mujmail.cz"),
                   ("guidobelix", "guidobelix@hotmail.it")]

    PLUGIN_DOMAIN = "easybytez.com"
