#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.1"
__author__ = "theRedMercury"

from resources.lib.api.api import API, get_torrest_plugin_url, get_stream_info_video, URL_API_SERVER
from resources.lib.utils import get_setting


class AnimeAPI:
    types = "animes"
    type_season = "show"


    def __init__(self):
        pass

    @staticmethod
    def get_animes(plugin, page, sort_request, genre):
        for dom in URL_API_SERVER:
            reply = API.get_list(plugin.pct_plugin.utils, dom, AnimeAPI.types, page, genre, sort_request)
            if reply is not None:
                return AnimeAPI.populate_shows(plugin, reply)

        return []

    @staticmethod
    def search(plugin, keyword):
        for dom in URL_API_SERVER:
             reply  = API.get_search(plugin.pct_plugin.utils, dom, AnimeAPI.types, keyword)
             if reply is not None:
                return AnimeAPI.populate_shows(plugin, reply)

        return []

    @staticmethod
    def get_animes_episodes(plugin, id_show, season):

        for dom in URL_API_SERVER:
            reply  = API.get_list_show_all(plugin.pct_plugin.utils, dom, AnimeAPI.type_season, id_show)
            if reply is not None:
                return AnimeAPI.populate_episodes(plugin, reply, season)
        

    @staticmethod
    def populate_shows(plugin, list_json_reply):
        items = []
        for result in list_json_reply:
            item = {
                "label": f"{result.get('title')} ({result.get('num_seasons')} seasons)",
                "icon": result.get('images').get('poster'),
                "thumbnail": result.get('images').get('poster'),
                "properties": {
                    "fanart_image": result.get('images').get('fanart').replace('/w500/', '/original/'),
                },

                "info": {
                    'mediatype': 'Anime',
                    'title': result.get('title'),
                    'tagline': result.get('num_seasons'),
                    'year': int(result.get('year')),
                    'genre': ', '.join(genre for genre in result.get('genres', [])) or None,
                    'rating': float(int(result.get('rating').get('percentage')) / 10),
                    'votes': result.get('rating').get('votes'),
                    'imdbnumber': result.get('imdb_id'),
                    'code': result.get('imdb_id'),
                    'plot': result.get('synopsis'),
                    'plotoutline': result.get('synopsis'),
                },

                "path": plugin.url_for("tv_shows.list_items_season",
                                       id_show=result.get('imdb_id'),
                                       num_seasons=result.get('num_seasons'),
                                       fanart=result.get('images').get('fanart').replace('/w500/', '/original/')),
            }

            items.append(item)
        return items

    @staticmethod
    def populate_episodes(plugin, json_reply, season):
        items = []

        quality_ask = get_setting("movies_quality") or '4k'
        quality_ask = '2160p' if quality_ask == '4k' else quality_ask

        for episode in json_reply.get('episodes'):
            if int(episode.get('season')) == int(season):

                stats_torrents = ""
                stats_torrents_full = ""
                subtitles = list(json_reply.get('exist_translations')) or ['en']
                quality = sorted(list(episode.get('torrents').keys()), key=lambda x: int(x[:-1] if len(x) > 1 else x),
                                 reverse=True) or []

                quality_found = quality_ask if quality_ask in episode.get('torrents').keys() else quality[0]

                for q in quality:
                    stats_torrents += f"{str(q).ljust(5, ' ')} | S({episode.get('torrents').get(q).get('seeds')}) / P({episode.get('torrents').get(q).get('peers')})\n"
                for q in quality:
                    stats_torrents_full += f"{str(q).ljust(5, ' ')} | Seed({episode.get('torrents').get(q).get('seeds')}) / Peer({episode.get('torrents').get(q).get('peers')})\n"

                stats_torrents_full += "lang : " + json_reply.get('contextLocale') + "\n"  # or original_language
                stats_torrents_full += "sub : " + ', '.join(subtitles) + "\n"

                magnet_url = episode.get('torrents').get(quality_found).get('url')

                menu = []
                for q in quality:
                    menu.append((f"Play {q}", get_torrest_plugin_url(episode.get('torrents').get(q).get('url'), True)))

                item = {
                    "label": f"{episode.get('episode')} : {episode.get('title')}",
                    "icon": json_reply.get('images').get('poster'),
                    "thumbnail": json_reply.get('images').get('poster'),
                    "properties": {
                        "fanart_image": json_reply.get('images').get('fanart').replace('/w500/', '/original/'),
                    },

                    "info": {
                        'mediatype': 'episode',
                        'season': episode.get('season'),
                        'episode': episode.get('episode'),
                        'plot': stats_torrents_full + (episode.get('overview') or ""),
                        'imdbnumber': json_reply.get('imdb_id'),
                        'code': json_reply.get('imdb_id'),
                        'year': int(json_reply.get('year')),
                        'genre': ', '.join(genre for genre in json_reply.get('genres', [])) or None,
                        'rating': float(int(json_reply.get('rating').get('percentage')) / 10),
                        'votes': json_reply.get('rating').get('votes'),
                    },

                    "stream_info": {
                        "video": get_stream_info_video(quality_found),
                        "audio": {
                            "language": json_reply.get('contextLocale')
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

        items = sorted(items, key=lambda x: int(x.get('info').get('episode')))
        return items
