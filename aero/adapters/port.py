# -*- coding: utf-8 -*-
__author__ = 'nickl-'
__all__ = ('Port', )

from string import strip

from aero.__version__ import __version__
from .base import BaseAdapter


class Port(BaseAdapter):
    """
    Macports adapter.
    """
    def search(self, query):
        response = self._execute_command('search', query)[0]
        lst = list(line for line in response.splitlines() if line)
        if lst:
            return dict(map(
                self.__parse_search, zip(*[iter(lst)] * 2)
            ))
        return {}

    def __parse_search(self, result):
        key = result[0].split(' ', 1)
        return [
            self.package_name(key.pop(0)),
            key.pop() + u' ' + result[1]
        ]

    def install(self, query):
        self.shell('install', query)
        return {}

    def info(self, query):
        result = self.command('info', query)[0]
        result = result.replace(u'{} '.format(query), u'Version: ')
        return [map(
            strip, line.split(u': ', 1)
        ) for line in result.splitlines()]
