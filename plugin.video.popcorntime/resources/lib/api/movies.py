#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.1"
__author__ = "theRedMercury"

from resources.lib.api.api import API, get_torrest_plugin_url, get_youtube_plugin_url, get_stream_info_video, URL_API_SERVER
from resources.lib.utils import get_setting


class MovieApi:
    types = "movies"


    def __init__(self):
        pass

    @staticmethod
    def get_movies(pct_plugin, page, sort_request, genre):
        for dom in URL_API_SERVER:
            reply =  API.get_list(pct_plugin.utils, dom, MovieApi.types, page, genre, sort_request)
            if reply is not None:
                return MovieApi.populate_items(pct_plugin, reply)
        return []

    @staticmethod
    def search_movies(pct_plugin, keyword):
        for dom in URL_API_SERVER:
            reply =  API.get_search(pct_plugin.utils, dom, MovieApi.types, keyword)
            if reply is not None:
                return MovieApi.populate_items(pct_plugin, reply)
        return []

    @staticmethod
    def populate_items(pct_plugin, json_reply):

        first_l = get_setting("first_lang_video")
        second_l = get_setting("second_lang_video")
        quality_ask = get_setting("movies_quality") or '4k'

        quality_ask = '2160p' if quality_ask == '4k' else quality_ask

        items = []
        for result in json_reply:

            keys_language = list(result.get('torrents').keys()) or ['en']
            subtitles = list(result.get('exist_translations')) or ['en']
            quality = sorted([list(result.get('torrents').get(k).keys()) for k in result.get('torrents').keys()][0],
                             key=lambda x: int(x[:-1] if len(x) > 1 else x), reverse=True) or []

            language_found = keys_language[0]
            if first_l in keys_language:
                language_found = first_l
            elif second_l in keys_language:
                language_found = second_l

            quality_found = quality_ask if quality_ask in result.get('torrents').get(language_found).keys() else \
                quality[0]

            stats_torrents = ""
            stats_torrents_full = ""

            for lang in keys_language:
                for q in quality:
                    stats_torrents += f"{str(q).ljust(5, ' ')} : {result.get('torrents').get(lang).get(q).get('filesize')} | S({result.get('torrents').get(lang).get(q).get('seed')}) / P({result.get('torrents').get(lang).get(q).get('peer')})\n"

            stats_torrents += "lang : " + ', '.join(keys_language) + "\n"
            stats_torrents += "sub : " + ', '.join(subtitles) + "\n"

            for lang in keys_language:
                for q in quality:
                    stats_torrents_full += f"{str(q).ljust(5, ' ')} : {result.get('torrents').get(lang).get(q).get('filesize')} | Seed({result.get('torrents').get(lang).get(q).get('seed')}) / Peer({result.get('torrents').get(lang).get(q).get('peer')})\n"

            magnet_url = result.get('torrents').get(language_found).get(quality_found).get('url')

            # SUB MENU
            menu = []
            for q in quality:
                menu.append((f"Play {q}",
                             get_torrest_plugin_url(result.get('torrents').get(language_found).get(q).get('url'),
                                                    True)))

            item = {
                "label": result.get('title'),
                "icon": result.get('images').get('poster'),
                "thumbnail": result.get('images').get('poster'),
                "properties": {
                    "fanart_image": result.get('images').get('fanart').replace('/w500/', '/original/'),
                },

                "info": {
                    'mediatype': 'movie',
                    'title': result.get('title'),
                    'duration': int(result.get('runtime')) * 60 or 0,
                    'tagline': ' / '.join(quality),
                    'year': int(result.get('year')),
                    'genre': ', '.join(genre for genre in result.get('genres', [])) or None,
                    'rating': float(int(result.get('rating').get('percentage')) / 10),
                    'votes': result.get('rating').get('votes'),
                    'imdbnumber': result.get('imdb_id'),
                    'code': result.get('imdb_id'),
                    'mpaa': result.get('certification'),
                    'plot': (result.get('synopsis') or "") + "\n" + stats_torrents_full,
                    'plotoutline': stats_torrents + (result.get('synopsis') or ""),
                    'trailer': get_youtube_plugin_url(result.get('trailer')),
                },

                "stream_info": {
                    "video": get_stream_info_video(quality_found),
                    "audio": {
                        "language": ', '.join(keys_language)
                    },
                    'subtitle': {
                        'language': ', '.join(subtitles)
                    }
                },

                "context_menu": menu,
                "is_playable": True,
                "replace_context_menu": True,

                "path": get_torrest_plugin_url(magnet_url),
            }
            items.append(item)

        return items
