#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.0"
__author__ = "theRedMercury"

import os.path

import xbmcswift2

from resources.lib.api.api import API
from resources.lib.api.animes import AnimeAPI
from resources.lib.utils import get_media


class AnimeMenu(xbmcswift2.Module):

    def __init__(self, pct_plugin):
        super(AnimeMenu, self).__init__('plugin.video.popcorntime.menu.animes_m')

        self.pct_plugin = pct_plugin
        # decorators
        self.menu = self.route('/animes/')(self.menu)
        self.search = self.route('/animes/search')(self.search)

    def menu(self):
        items = [
            {'label': self.pct_plugin.tr('most_popular'),
             'icon': get_media("animes", "popular.png"),
             'thumbnail': get_media("animes", "popular.png"),
             'path': self.url_for('animes.list_items', sort_request="trending", explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('recently'),
             'icon': get_media("animes", "recently.png"),
             'thumbnail': get_media("animes", "recently.png"),
             'path': self.url_for('animes.list_items', sort_request="last_added", explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('rated'),
             'icon': get_media("animes", "rated.png"),
             'thumbnail': get_media("animes", "rated.png"),
             'path': self.url_for('animes.list_items', sort_request="rating", explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('genres'),
             'icon': get_media("animes", "genres.png"),
             'thumbnail': get_media("animes", "genres.png"),
             'path': self.url_for('animes.genres', explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('search'),
             'icon': get_media("animes", "search.png"),
             'thumbnail': get_media("animes", "search.png"),
             'path': self.url_for('animes_m.search', explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},
        ]
        return items

    def search(self):
        self.pct_plugin.utils.log.debug("go to search")
        query = self.keyboard(heading=self.pct_plugin.tr('search'))
        if query:
            self.plugin.redirect(self.url_for('animes.search', keyword=query, explicit=True))


class AnimeList(xbmcswift2.Module):

    def __init__(self, pct_plugin):
        super(AnimeList, self).__init__('plugin.video.popcorntime.menu.animes_m.animes')

        self.pct_plugin = pct_plugin

        # decorators
        self.list_items = self.route('/animes/list_items/<sort_request>/<genre>/<page>',
                                     options={'genre': 'all', 'page': '1'})(self.list_items)
        self.list_items_season = self.route('/animes/list_items_season/<id_show>/<num_seasons>/<fanart>',
                                            options={'fanart': ''})(self.list_items_season)
        self.list_items_episodes = self.route('/animes/list_items_episodes/<id_show>/<season>')(
            self.list_items_episodes)

        self.genres = self.route('/animes/genres')(self.genres)
        self.search = self.route('/animes/search/<keyword>')(self.search)

    def search(self, keyword):
        self.pct_plugin.utils.log.debug(f"search : {keyword} ")
        return AnimeAPI.search(self, keyword)

    def list_items(self, sort_request, genre, page):
        self.pct_plugin.utils.log.debug(f"list_items page : {page} - {genre} - {sort_request}")

        items = AnimeAPI.get_animes(self, page, sort_request, genre)

        next_page = str(int(page) + 1)
        self.pct_plugin.utils.log.debug(f"list_items int_page : {next_page} ")
        items.append(
            {'label': self.pct_plugin.tr('show_more'),
             'icon': get_media("animes", "more.png"),
             'thumbnail': get_media("animes", "more_thumbnail.png"),
             'path': self.url_for('animes.list_items', sort_request=sort_request, page=next_page, genre=genre,
                                  explicit=True),
             'offscreen': True},
        )
        return items

    def list_items_season(self, id_show, num_seasons, fanart):
        self.pct_plugin.utils.log.debug(f"list_items_season page : {id_show}")

        items = []
        for i in range(0, int(num_seasons)):
            item = {
                "label": f"season {i + 1}",
                "properties": {
                    "fanart_image": fanart,
                },
                "info": {
                    'mediatype': 'season',
                },
                "path": self.url_for("animes.list_items_episodes", id_show=id_show, season=(i + 1)),
            }
            items.append(item)
        return items

    def list_items_episodes(self, id_show, season):
        self.pct_plugin.utils.log.debug(f"list_items_episodes page : {id_show} - {season}")
        return AnimeAPI.get_animes_episodes(self, id_show, season)

    def genres(self):
        items = [
            {
                'label': self.pct_plugin.tr_id(key),
                'icon': get_media(os.path.join("animes", "genres"), f"{value}.png"),
                'thumbnail': get_media(os.path.join("animes", "genres"), f"{value}.png"),
                'path': self.url_for('animes.list_items', sort_request="trending", genre=value, explicit=True),
                "properties": {
                    "fanart_image": get_media("categories", "fanart.jpg"),
                },
                'offscreen': True
            } for key, value in API.genres.items()
        ]
        return items
