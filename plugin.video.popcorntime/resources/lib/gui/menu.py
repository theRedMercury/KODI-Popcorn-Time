#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.0"
__author__ = "theRedMercury"

import xbmcswift2

from resources.lib.utils import get_media


class MainMenu(xbmcswift2.Module):

    def __init__(self, pct_plugin):
        super(MainMenu, self).__init__('plugin.video.popcorntime.menu')

        self.pct_plugin = pct_plugin

        # decorators
        self.menu = self.route('/')(self.menu)

    def menu(self):
        items = [
            {
                'label': self.pct_plugin.tr('movie'),
                'icon': get_media("categories", "Movies.png"),
                'thumbnail': get_media("categories", "Movies.png"),
                'path': self.url_for('movie_m.menu', explicit=True),
                "properties": {
                    "fanart_image": get_media("categories", "fanart.jpg"),
                },
                'offscreen': True
            },
            {
                'label': self.pct_plugin.tr('tv_shows'),
                'icon': get_media("categories", "TVShows.png"),
                'thumbnail': get_media("categories", "TVShows.png"),
                'path': self.url_for('tv_show_m.menu', explicit=True),
                "properties": {
                    "fanart_image": get_media("categories", "fanart.jpg"),
                },
                'offscreen': True
            },
            {
                'label': self.pct_plugin.tr('anime'),
                'icon': get_media("categories", "TVShows.png"),
                'thumbnail': get_media("categories", "TVShows.png"),
                'path': self.url_for('animes_m.menu', explicit=True),
                "properties": {
                    "fanart_image": get_media("categories", "fanart.jpg"),
                },
                'offscreen': True
            },
        ]
        return items
