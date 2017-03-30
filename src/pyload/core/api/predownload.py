# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import io
import os
import re
from builtins import str
from itertools import chain

from future import standard_library
standard_library.install_aliases()

from pyload.utils import parse
from pyload.utils.purge import uniqify

from ..datatype.check import OnlineCheck
from ..datatype.init import DownloadStatus, LinkStatus, Permission
from ..network.request import get_url
from .base import BaseApi
from .init import Api, requireperm


_re_urlmatch = re.compile(
    r'((https?|ftps?|xdcc|sftp):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+\-=\\\.&]*)',
    flags=re.I)


class PreDownloadApi(BaseApi):
    """
    All kind of methods to parse links or retrieve online status.
    """
    __slots__ = []

    @requireperm(Permission.Add)
    def parse_links(self, links):
        """
        Gets urls and returns pluginname mapped to list of matching urls.

        :param links:
        :return: {plugin: urls}
        """
        data, crypter = self.pyload.pgm.parse_urls(links)
        plugins = {}

        for url, plugin in chain(data, crypter):
            if plugin in plugins:
                plugins[plugin].append(url)
            else:
                plugins[plugin] = [url]

        return plugins

    @requireperm(Permission.Add)
    def check_links(self, links):
        """
        Initiates online status check, will also decrypt files.

        :param links:
        :return: initial set of data as :class:`OnlineCheck` instance containing the result id
        """
        hoster, crypter = self.pyload.pgm.parse_urls(links)

        # TODO: withhold crypter, derypt or add later
        # initial result does not contain the crypter links
        tmp = [(url, LinkStatus(url, url, -1, DownloadStatus.Queued, pluginname))
               for url, pluginname in hoster]
        data = parse.packs(tmp)
        rid = self.pyload.thm.create_result_thread(
            self.primary_uid, hoster + crypter)

        return OnlineCheck(rid, data)

    @requireperm(Permission.Add)
    def check_container(self, filename, data):
        """
        Checks online status of urls and a submitted container file

        :param filename: name of the file
        :param data: file content
        :return: :class:`OnlineCheck`
        """
        file = os.path.join(self.pyload.config.get(
            'general', 'storage_folder'), "tmp_{0}".format(filename))
        with io.open(file, mode='wb') as fp:
            fp.write(str(data))
            return self.check_links([fp.name])

    @requireperm(Permission.Add)
    def check_html(self, html, url):
        """
        Parses html content or any arbitrary text for links and returns result of `check_urls`

        :param html: html source
        :return:
        """
        urls = []
        if html:
            urls += [x[0] for x in _re_urlmatch.findall(html)]
        if url:
            page = get_url(url)
            urls += [x[0] for x in _re_urlmatch.findall(page)]

        return self.check_links(uniqify(urls))

    @requireperm(Permission.Add)
    def poll_results(self, rid):
        """
        Polls the result available for ResultID

        :param rid: `ResultID`
        :return: `OnlineCheck`, if rid is -1 then there is no more data available
        """
        result = self.pyload.thm.get_info_result(rid)
        if result and result.owner == self.primary_uid:
            return result.to_api_data()

    @requireperm(Permission.Add)
    def generate_packages(self, links):
        """
        Parses links, generates packages names from urls

        :param links: list of urls
        :return: package names mapped to urls
        """
        result = parse.packs((x, x) for x in links)
        return result